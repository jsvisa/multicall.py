from typing import Union, Dict, Tuple, List
from functools import lru_cache
from eth_abi.abi import encode, decode
from eth_utils.abi import (
    function_signature_to_4byte_selector,
    function_abi_to_4byte_selector,
    collapse_if_tuple,
)
from eth_utils.hexadecimal import encode_hex, decode_hex


@lru_cache(maxsize=4096)
def parse_signature(signature: str) -> Tuple[str, List[str], List[str]]:
    """
    Breaks 'func(address)(uint256)' into ['func', ['address'], ['uint256']]
    """
    parts: List[str] = []
    stack: List[str] = []
    start: int = 0
    for end, character in enumerate(signature):
        if character == "(":
            stack.append(character)
            if not parts:
                parts.append(signature[start:end])
                start = end
        if character == ")":
            stack.pop()
            if not stack:  # we are only interested in outermost groups
                parts.append(signature[start : end + 1])
                start = end + 1
    function = "".join(parts[:2])
    input_types = parse_typestring(parts[1])
    output_types = parse_typestring(parts[2])
    return function, input_types, output_types


def parse_typestring(typestring: str) -> List[str]:
    if typestring == "()":
        return []
    parts = []
    part = ""
    inside_tuples = 0
    for character in typestring[1:-1]:
        if character == "(":
            inside_tuples += 1
        elif character == ")":
            inside_tuples -= 1
        elif character == "," and inside_tuples == 0:
            parts.append(part)
            part = ""
            continue
        part += character
    parts.append(part)
    return parts


class Signature:
    """
    Encode/Decode function text signature or ABI,
    eg:
        function text signature:
            balanceOf(address)(uint256)
    or ABI
        {
            "name": "balanceOf",
            "inputs": [{"name": "account", "type": "address"}],
            "outputs": [{"name": "", "type": "uint256"}],
        }

    """

    def __init__(self, signature: Union[str, Dict]):
        self.signature = signature
        if isinstance(signature, str):
            parts = parse_signature(signature.strip().replace(" ", ""))

            self.function = parts[0]
            self.input_types = parts[1]
            self.output_types = parts[2]
            self.fourbyte = function_signature_to_4byte_selector(self.function)

        elif isinstance(signature, dict):
            self.fourbyte = function_abi_to_4byte_selector(signature)
            self.input_types = [
                collapse_if_tuple(abi) for abi in signature.get("inputs", [])
            ]
            self.output_types = [
                collapse_if_tuple(abi) for abi in signature.get("outputs", [])
            ]
            self.function = "{}({})".format(
                signature["name"], ",".join(self.input_types)
            )

    def encode_data(self, args=None):
        data = self.fourbyte
        if args:
            data += encode(self.input_types, args)
        return encode_hex(data)

    def decode_data(self, data: Union[str, bytes], ignore_error: bool = False):
        if isinstance(data, str):
            data = decode_hex(data)
        try:
            decoded = decode(self.output_types, data)
        except Exception as ex:
            if ignore_error is True:
                return None
            else:
                msg = f"failed to decode data: {data} of signature: {self.signature}"
                raise Exception(msg) from ex

        # decode returns a tuple,
        # if there are only one return value,
        # then we extract that value out
        return decoded if len(decoded) > 1 else decoded[0]
