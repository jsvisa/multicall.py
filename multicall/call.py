import hashlib
import logging
from typing import Optional, Sequence, Union, Dict, Any
from eth_utils.address import to_checksum_address
from .signature import Signature


class Call:
    def __init__(
        self,
        target: str,
        function: Union[str, dict],
        args: Optional[Sequence] = None,
        request_id: Optional[Union[int, str]] = None,
        block_id: Union[int, str] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.target = to_checksum_address(target)
        self.function = function
        self.args = args
        self.signature = Signature(self.function)
        if request_id is None:
            request_id = hashlib.md5(f"{target}:{function}:{args}".encode()).hexdigest()
        self.request_id = request_id
        self.block_id = block_id
        self.ignore_error = ignore_error
        self.logger = logger or logging.getLogger(__name__)
        self.gas_limit = gas_limit

    @property
    def calldata(self):
        return self.signature.encode_data(self.args)

    def decode(self, rpc_res: Dict, ignore_error: bool = False) -> Any:
        ignore_error = ignore_error or self.ignore_error
        request_msg = "target={} function={} args={} input_types={} output_types={} block_id={} rpc_res={}".format(  # noqa
            self.target,
            self.function,
            self.args,
            self.signature.input_types,
            self.signature.output_types,
            self.block_id,
            rpc_res,
        )
        self.logger.debug(request_msg)
        if "error" in rpc_res:
            if ignore_error:
                err_msg = f"get the json-rpc error in request: {request_msg}"
                self.logger.error(err_msg)
                return None
            else:
                raise ValueError(rpc_res)

        return self.signature.decode_data(rpc_res["result"], ignore_error)

    def __call__(
        self,
        block_id: Optional[Union[str, int]] = None,
        gas_limit: Optional[int] = None,
    ):
        block = block_id or self.block_id or "latest"
        gas = gas_limit or self.gas_limit

        params = {"to": self.target, "data": self.calldata}
        if gas:
            params["gas"] = hex(gas)

        return {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [
                params,
                hex(block) if isinstance(block, int) else block,
            ],
            "id": self.request_id,
        }
