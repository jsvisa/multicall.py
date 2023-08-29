from typing import Union, Dict
from functools import lru_cache
from eth_abi.abi import encode, decode
from eth_utils.abi import (
    function_signature_to_4byte_selector,
    function_abi_to_4byte_selector,
    collapse_if_tuple,
)
from eth_utils.hexadecimal import encode_hex, decode_hex


@lru_cache(maxsize=4096)
def parse_signature(signature: str):
    """
    Breaks 'func(address)(uint256)' into ['func', '(address)', '(uint256)']
    """
    parts = []
    stack = []
    start = 0
    for end, letter in enumerate(signature):
        if letter == "(":
            stack.append(letter)
            if not parts:
                parts.append(signature[start:end])
                start = end
        if letter == ")":
            stack.pop()
            if not stack:
                parts.append(signature[start : end + 1])
                start = end + 1
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

            self.input_types = parts[1]
            self.output_types = parts[2]
            function = "".join(parts[:2])
            self.fourbyte = function_signature_to_4byte_selector(function)

        elif isinstance(signature, dict):
            self.fourbyte = function_abi_to_4byte_selector(signature)
            self.input_types = "({})".format(
                ",".join(collapse_if_tuple(abi) for abi in signature.get("inputs", []))
            )
            self.output_types = "({})".format(
                ",".join(collapse_if_tuple(abi) for abi in signature.get("outputs", []))
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
            decoded = decode(self.output_types, data)[0]
        except Exception as ex:
            if ignore_error is True:
                return None
            else:
                msg = f"failed to decode data: {data} of signature: {self.signature}"
                raise Exception(msg) from ex

        return decoded if len(decoded) > 1 else decoded[0]
