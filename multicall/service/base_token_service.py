from typing import Optional
from multicall import Call


class BaseTokenService:
    def name(
        self,
        token: str,
        request_id: Optional[str] = None,
        ignore_error: bool = False,
    ) -> Call:
        return Call(
            target=token,
            function="name()(string)",
            request_id=request_id,
            ignore_error=ignore_error,
        )

    def symbol(
        self,
        token: str,
        request_id: Optional[str] = None,
        ignore_error: bool = False,
    ) -> Call:
        return Call(
            target=token,
            function="symbol()(string)",
            request_id=request_id,
            ignore_error=ignore_error,
        )
