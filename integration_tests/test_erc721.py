import os
import unittest

from multicall import Multicall, Call
from multicall.service.erc721_service import Erc721Service


class TestErc721(unittest.TestCase):
    token_address = "0x2abb22d74dbc2b0f3c9bac9f173ef35ddb2c0809"
    owner = "0xbc737060177cb65be931a46d7142848fe694c8e7"
    token_id = 1
    block_id = 14200879
    erc721_service = Erc721Service()
    mc = Multicall(os.environ["ETHEREUM_PROVIDER_URI"])

    def test_token_by_index(self):
        excepted = [{"request_id": self.token_address, "result": 1}]
        call = self.erc721_service.tokenByIndex(
            token=self.token_address,
            index=0,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_balance(self):
        excepted = [{"request_id": self.token_address, "result": 7}]

        call = self.erc721_service.balanceOf(
            token=self.token_address,
            owner=self.owner,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_ownerOf(self):
        excepted = [
            {
                "request_id": self.token_address,
                "result": self.owner,
            }
        ]
        call = self.erc721_service.ownerOf(
            token=self.token_address,
            token_id=self.token_id,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_token_uri(self):
        excepted = [
            {
                "request_id": self.token_address,
                "result": "https://lumen.mypinata.cloud/ipfs/QmWtg4Gp5fe4EWaVE1jRhUqewQi2Ss7Q1ettxQmNVQ1byJ",
            }
        ]
        call = self.erc721_service.tokenURI(
            token=self.token_address,
            token_id=self.token_id,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_total_supply(self):
        excepted = [
            {
                "request_id": self.token_address,
                "result": 7460,
            }
        ]
        call = self.erc721_service.totalSupply(
            token=self.token_address,
            request_id=self.token_address,
            block_id=self.block_id,
        )

        result = self.mc.agg([call])
        assert result == excepted

    def test_get_total_supply_of_not_implemented_token(self):
        # ens = "0xc18360217d8f7ab5e7c516566761ea12ce7f9d72"
        token = "0x81A8e12626C51dC931E2d81A0430AB9dC6fe6fC7"
        call = Call(target=token, function="totalSupply()(uint256)", ignore_error=False)
        self.assertRaises(Exception, lambda: self.mc.agg([call]))

        self.mc.agg([call], ignore_error=True)

        call = Call(target=token, function="totalSupply()(uint256)", ignore_error=True)
        self.mc.agg([call], ignore_error=False)
        self.mc.agg([call], ignore_error=True)
