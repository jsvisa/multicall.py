from typing import Optional, Union
from multicall import Call
from eth_utils.address import to_checksum_address
from multicall.service.base_token_service import BaseTokenService


class Erc20Service(BaseTokenService):
    def balanceOf(
        self,
        token: str,
        owner: str,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        return Call(
            target=token,
            function="balanceOf(address)(uint256)",
            args=[to_checksum_address(owner)],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def decimals(
        self,
        token: str,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        return Call(
            target=token,
            function="decimals()(uint8)",
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def totalSupply(
        self,
        token: str,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        return Call(
            target=token,
            function="totalSupply()(uint256)",
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def allowance(
        self,
        token: str,
        owner: str,
        spender: str,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        return Call(
            target=token,
            function="allowance(address,address)(uint256)",
            args=[to_checksum_address(owner), to_checksum_address(spender)],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )
