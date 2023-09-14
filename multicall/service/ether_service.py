from typing import Union, List, Dict, Any, Optional
from multicall import Multicall, BalanceCall
from requests import Session
from eth_utils.address import to_checksum_address

from .erc20_service import Erc20Service


class EtherService:
    def __init__(
        self,
        provider_uri: str,
        mc: Optional[Multicall] = None,
        session: Optional[Session] = None,
    ):
        self.mc = mc or Multicall(provider_uri, session=session)
        self.erc20_service = Erc20Service()

    def get_balance(
        self,
        accounts: Union[str, List[str]],
        block_id: Union[str, int] = "latest",
        batch_size: int = -1,
        max_workers: int = 1,
        keep_zero_balance: bool = False,
    ) -> List[Dict[str, Any]]:
        if isinstance(accounts, str):
            accounts = [accounts]

        calls = [
            BalanceCall(to_checksum_address(addr), request_id=addr)
            for addr in set(a.lower() for a in accounts)
        ]
        result = self.mc.agg(
            calls,
            block_id=block_id,
            as_dict=True,
            ignore_error=True,
            batch_size=batch_size,
            max_workers=max_workers,
        )
        assert isinstance(result, dict)

        return [
            {
                "token": "0x0000000000000000000000000000000000000000",
                "asset": "ETH",
                "account": key,
                "value": val,
            }
            for key, val in result.items()
            if val is not None and (val > 0 or keep_zero_balance is True)
        ]

    def get_token_balance(
        self,
        tokens: Union[str, List[str]],
        accounts: Union[str, List[str]],
        block_id: Union[str, int] = "latest",
        batch_size: int = -1,
        max_workers: int = 1,
        ignore_error: bool = False,
        keep_zero_balance: bool = False,
    ) -> List[Dict[str, Any]]:
        if isinstance(tokens, str):
            tokens = [tokens]
        if isinstance(accounts, str):
            accounts = [accounts]

        calls = [
            self.erc20_service.balanceOf(
                token,
                addr,
                request_id=f"{token},{addr}",
                ignore_error=ignore_error,
            )
            for token in set(t.lower() for t in tokens)
            for addr in set(a.lower() for a in accounts)
        ]
        result = self.mc.agg(
            calls,
            block_id=block_id,
            as_dict=True,
            ignore_error=True,
            batch_size=batch_size,
            max_workers=max_workers,
        )
        assert isinstance(result, dict)

        return [
            {
                "token": key.split(",")[0],
                "account": key.split(",")[1],
                "value": val,
            }
            for key, val in result.items()
            if val is not None and (val > 0 or keep_zero_balance is True)
        ]
