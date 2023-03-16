from typing import Optional, Union
from multicall import Call
from eth_utils.address import to_checksum_address
from multicall.service.base_token_service import BaseTokenService


class Erc721Service(BaseTokenService):
    def balanceOf(
        self,
        token: str,
        owner: str,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = True,
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

    def tokenURI(
        self,
        token: str,
        token_id: int,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = True,
        gas_limit: Optional[int] = None,
    ) -> Call:
        return Call(
            target=token,
            function="tokenURI(uint256)(string)",
            args=[token_id],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def ownerOf(
        self,
        token: str,
        token_id: int,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = True,
        gas_limit: Optional[int] = None,
    ) -> Call:
        if token_id is None:
            raise Exception("getting erc721 token owner of required token id")
        return Call(
            target=token,
            function="ownerOf(uint256)(address)",
            args=[token_id],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def tokenByIndex(
        self,
        token: str,
        index: int,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = True,
        gas_limit: Optional[int] = None,
    ):
        if index is None:
            raise Exception("getting erc721 token by index required index")
        return Call(
            target=token,
            function="tokenByIndex(uint256)(uint256)",
            args=[index],
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
        ignore_error: bool = True,
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
