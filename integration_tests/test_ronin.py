import os
from multicall import Multicall, Call


class TestRoninChain:
    def test_multicall_with_batch_size_1(self):
        token = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
        mc = Multicall(os.environ["RONIN_PROVIDER_URI"])

        calls = [
            Call(
                token,
                "balanceOf(address)(uint256)",
                args=("0x030e37ddd7df1b43db172b23916d523f1599c6cb",),
                request_id="balanceOf",
            ),
            Call(
                token,
                "name()(string)",
                request_id="name",
            ),
            Call(
                token,
                "symbol()(string)",
                request_id="symbol",
            ),
        ]

        result = mc.agg(calls, as_dict=True, batch_size=1, block_id="latest")
        assert isinstance(result, dict)
        assert set(result.keys()) == set(["balanceOf", "name", "symbol"])

        result = mc.agg(
            calls, as_dict=True, batch_size=1, max_workers=5, block_id="latest"
        )
        assert isinstance(result, dict)
        assert set(result.keys()) == set(["balanceOf", "name", "symbol"])
