from itertools import chain
from typing import List, Dict, Tuple, Optional, Any, Union
from eth_abi.abi import decode
from eth_utils.abi import collapse_if_tuple


def collapse_if_tuple_with_name(abi: Dict[str, Any], is_event=False) -> str:
    """
    Converts a tuple from a dict to a parenthesized list of its types.
    Copy from eth_utils.abi

    >>> from eth_utils.abi import collapse_if_tuple
    >>> collapse_if_tuple(
    ...     {
    ...         'components': [
    ...             {'name': 'anAddress', 'type': 'address'},
    ...             {'name': 'anInt', 'type': 'uint256'},
    ...             {'name': 'someBytes', 'type': 'bytes'},
    ...         ],
    ...         'type': 'tuple',
    ...     }
    ... )
    '(address,uint256,bytes)'

    >>> collapse_if_tuple_with_name(
    ...     {
    ...         'components': [
    ...             {'name': 'anAddress', 'type': 'address'},
    ...             {'name': 'anInt', 'type': 'uint256'},
    ...             {'name': 'someBytes', 'type': 'bytes'},
    ...         ],
    ...         'type': 'tuple',
    ...     }
    ... )
    '(address anAddress, uint256 anInt, bytes someBytes)'
    """
    typ = abi["type"]
    if not isinstance(typ, str):
        raise TypeError(
            "The 'type' must be a string, but got %r of type %s" % (typ, type(typ))
        )
    elif not typ.startswith("tuple"):
        return "{indexed}{typ} {name}".format(
            indexed="index " if is_event is True and abi.get("indexed") is True else "",
            typ=typ,
            name=abi.get("name", ""),
        )

    delimited = ", ".join(collapse_if_tuple_with_name(c) for c in abi["components"])
    # Whatever comes after "tuple" is the array dims.  The ABI spec states that
    # this will have the form "", "[]", or "[k]".
    array_dim = typ[5:]
    collapsed = "({delimited}){array_dim}{name}".format(
        delimited=delimited, array_dim=array_dim, name=abi.get("name", "")
    )

    return collapsed


def abi_to_signature_with_arguments(abi: Dict[str, Any]) -> str:
    function_signature = "{fn_name}({fn_input_types})".format(
        fn_name=abi["name"],
        fn_input_types=", ".join(
            [
                collapse_if_tuple_with_name(abi_input)
                for abi_input in abi.get("inputs", [])
            ]
        ),
    )
    return function_signature


def convert_bytes_array(val):
    if isinstance(val, (list, tuple)):
        return [convert_bytes_array(v) for v in val]
    # base case: single bytes value
    if isinstance(val, bytes):
        return val.hex()
    return val


def zip_if_tuple(abi: Dict, value) -> Dict:
    typ = abi["type"]
    name = abi["name"]
    if typ.startswith("byte"):
        # handle multiple dimensional byte arrays
        if typ.endswith("]"):
            values = convert_bytes_array(value)
            return {name: values}
        else:
            return {name: value.hex()}
    if not typ.startswith("tuple"):
        return {name: value}

    # we need to extract the sub-values from a tuple array:
    # tuple[] -> 1 tuple[][] -> 2 tuple[][][] -> 3
    # the ABI for those tuple arraies are still the compated one:
    # eg:
    # {
    #     "name": "doHardWork",
    #     "type": "function",
    #     "inputs": [
    #         {
    #             "name": "dhwParams",
    #             "type": "tuple",
    #             "components": [
    #                 {
    #                     "name": "swapInfo",
    #                     "type": "tuple[][][]",
    #                     "components": [
    #                         {"name": "swapTarget", "type": "address"},
    #                         {"name": "token", "type": "address"},
    #                         {"name": "swapCallData", "type": "bytes"},
    #                     ],
    #                     "internalType": "struct SwapInfo[][][]",
    #                 }
    #             ],
    #         }
    #     ],
    # }
    # so we need to iterate the input data to extract the sub-values
    n_dims = (len(typ) - len("tuple")) // 2
    subabi = abi["components"]
    return {name: extract_sub_values(subabi, value, n_dims)}


def extract_sub_values(abi: List[Dict], value: Any, n_dims: int) -> Union[List, Dict]:
    if n_dims == 0:
        subvalue = {}
        for idx, sa in enumerate(abi):
            subvalue.update(zip_if_tuple(sa, value[idx]))
        return subvalue

    return [extract_sub_values(abi, sub, n_dims - 1) for sub in value]


def eth_decode_input(func_abi: Dict, data) -> Tuple:
    if "name" not in func_abi or func_abi.get("type") != "function":
        return (None, None)

    inputs = func_abi.get("inputs", [])
    func_sign = [collapse_if_tuple(i) for i in inputs]
    func_text = "{}({})".format(func_abi["name"], ",".join(func_sign))

    decoded = decode(func_sign, bytes(bytearray.fromhex(data[10:])))
    parameter = {}
    for idx, value in enumerate(decoded):
        parameter.update(zip_if_tuple(inputs[idx], value))

    return func_text, parameter


def eth_decode_log(event_abi: Dict, topics: List[str], data: str) -> Tuple:
    if "name" not in event_abi or event_abi.get("type") != "event":
        return (None, None)

    # rewrite the indexed columns first
    indexed, normal = [], []
    if "inputs" in event_abi:
        for input in event_abi.get("inputs", []):
            if input.get("indexed") is True:
                indexed.append(collapse_if_tuple(input))
            else:
                normal.append(collapse_if_tuple(input))
    indexed_values = decode(
        indexed, bytes(bytearray.fromhex("".join(e[2:] for e in topics[1:])))
    )
    data_values = decode(normal, bytes(bytearray.fromhex(data[2:])))

    return indexed_values, data_values


def eth_decode_log_as_dict(abi: Dict, topics: List[str], data: str) -> Optional[Dict]:
    indexed_values, data_values = eth_decode_log(abi, topics, data)
    if None in (indexed_values, data_values):
        return None

    indexed_names, data_names = [], []
    byte_names = []
    if "inputs" in abi:
        for _in in abi.get("inputs", []):
            name = _in["name"]
            if _in.get("indexed") is True:
                indexed_names.append(name)
            else:
                data_names.append(name)
            if _in["type"].startswith("byte"):
                byte_names.append(name)

    parameter = dict(
        chain(zip(indexed_names, indexed_values), zip(data_names, data_values))
    )
    for key in byte_names:
        val = parameter[key]
        if isinstance(val, tuple):
            parameter[key] = tuple([e.hex() for e in val])
        elif isinstance(val, bytes):
            parameter[key] = val.hex()

    return parameter
