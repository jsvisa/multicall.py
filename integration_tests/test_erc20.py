import os
from multicall import Multicall
from multicall.service.erc20_service import Erc20Service


class TestErc20:
    token_address = "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"
    owner = "0x65b654b8ebe64ed62b05ea3cbdd3d20f6ca33880"
    block_id = 13450206
    erc20_service = Erc20Service()
    mc = Multicall(os.environ["ETHEREUM_PROVIDER_URI"])

    def test_get_balance(self):
        excepted = [
            {
                "request_id": self.token_address,
                "result": 6266076220000000000,
            }
        ]

        call = self.erc20_service.balanceOf(
            token=self.token_address,
            owner=self.owner,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted
