from typing import Dict, Optional
from requests import Session
from multicall import Multicall, Call


def implements(result: Dict, method: str) -> bool:
    return result[method] is not None


ETH_0 = "0x" + "0" * 40
ETH_1 = "0x" + "1" * 40


class TokenService:
    def __init__(self, provider_uri: str, session: Optional[Session] = None):
        self.mc = Multicall(provider_uri, session=session)

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
    # https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol
    def is_erc20_token(self, token: str) -> bool:
        calls = [
            Call(token, "totalSupply()", request_id="totalSupply"),
            Call(
                token,
                "balanceOf(address)",
                args=(ETH_0,),
                request_id="balanceOf",
            ),
            Call(
                token,
                "transfer(address,uint256)",
                args=(ETH_0, 0),
                request_id="transfer",
            ),
            Call(
                token,
                "transferFrom(address,address,uint256)",
                args=(ETH_0, ETH_1, 0),
                request_id="transferFrom",
            ),
            Call(
                token, "approve(address,uint256)", args=(ETH_0, 0), request_id="approve"
            ),
            Call(
                token,
                "allowance(address,address)",
                args=(ETH_0, ETH_0),
                request_id="allowance",
            ),
        ]
        result = self.mc.agg(calls, as_dict=True, ignore_error=True)
        assert isinstance(result, dict)

        return (
            implements(result, "totalSupply")
            and implements(result, "balanceOf")
            and implements(result, "transfer")
            and implements(result, "transferFrom")
            and implements(result, "approve")
            and implements(result, "allowance")
        )

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md
    # https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/IERC721.sol
    # Doesn't check the below ERC721 methods to match CryptoKitties contract
    # getApproved(uint256)
    # setApprovalForAll(address,bool)
    # isApprovedForAll(address,address)
    # transferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256,bytes)
    def is_erc721_token(self, token: str) -> bool:
        calls = [
            Call(token, "balanceOf(address)", args=(ETH_0,), request_id="balanceOf"),
            Call(token, "ownerOf(uint256)", args=(1,), request_id="ownerOf"),
            Call(
                token,
                "transfer(address,uint256)",
                args=(ETH_0, 1),
                request_id="transfer",
            ),
            Call(
                token,
                "transferFrom(address,address,uint256)",
                args=(ETH_0, ETH_1, 0),
                request_id="transferFrom",
            ),
            Call(
                token, "approve(address,uint256)", args=(ETH_0, 0), request_id="approve"
            ),
        ]
        result = self.mc.agg(calls, as_dict=True, ignore_error=True)
        assert isinstance(result, dict)

        return (
            implements(result, "balanceOf")
            and implements(result, "ownerOf")
            and any(
                [
                    implements(result, "transfer"),
                    implements(result, "transferFrom"),
                ]
            )
            and implements(result, "approve")
        )
