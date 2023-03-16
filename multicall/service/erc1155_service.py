from typing import Optional, Union, List
from multicall import Call
from eth_utils.address import to_checksum_address
from multicall.service.base_token_service import BaseTokenService


class Erc1155Service(BaseTokenService):
    def balanceOf(
        self,
        token: str,
        owner: str,
        token_id: int,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        if token_id is None:
            raise Exception("getting erc1155 token balance required token id")
        return Call(
            target=token,
            function="balanceOf(address, uint256)(uint256)",
            args=[to_checksum_address(owner), token_id],
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
            raise Exception("getting erc1155 token by index required index")
        return Call(
            target=token,
            function="tokenByIndex(uint256)(uint256)",
            args=[index],
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
        ignore_error: bool = False,
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

    def uri(
        self,
        token: str,
        token_id: Optional[int],
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
    ) -> Call:
        if token_id is None:
            function = "uri()(string)"
            args = None
        else:
            function = "uri(uint256)(string)"
            args = [token_id]

        return Call(
            target=token,
            function=function,
            args=args,
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
        )

    def ownerOf(
        self,
        token: str,
        token_id: int,
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        if token_id is None:
            raise Exception("getting erc1155 token owner of require token id")
        return Call(
            target=token,
            function="ownerOf(uint256)(address)",
            args=[token_id],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )

    def balanceOfBatch(
        self,
        token: str,
        owners: List[str],
        token_ids: List[int],
        request_id: Optional[str] = None,
        block_id: Union[str, int] = "latest",
        ignore_error: bool = False,
        gas_limit: Optional[int] = None,
    ) -> Call:
        if owners is None or token_ids is None:
            raise Exception("owners or token ids are None")
        if len(owners) != len(token_ids):
            raise Exception(
                "the given address length does not match the length of the token id"
            )
        return Call(
            target=token,
            function="balanceOfBatch(address[], uint256[])(uint256[])",
            args=[[to_checksum_address(owner) for owner in owners], token_ids],
            request_id=request_id,
            block_id=block_id,
            ignore_error=ignore_error,
            gas_limit=gas_limit,
        )
