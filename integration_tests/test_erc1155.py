import os
from multicall import Multicall
from multicall.service.erc1155_service import Erc1155Service


class TestErc1155:
    token_address = "0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c"
    owner = "0x59bd01facd1035f2b89102a23110411934470eef"
    token_id = 202808290684879324224171266029333854027776
    block_id = 13729208
    erc1155_service = Erc1155Service()
    mc = Multicall(os.environ["ETHEREUM_PROVIDER_URI"])

    def test_get_balance(self):

        excepted = [{"request_id": self.token_address, "result": 1}]

        call = self.erc1155_service.balanceOf(
            token=self.token_address,
            owner=self.owner,
            token_id=self.token_id,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_balance_batch(self):

        excepted = [{"request_id": self.token_address, "result": (1,)}]

        call = self.erc1155_service.balanceOfBatch(
            token=self.token_address,
            owners=[self.owner],
            token_ids=[self.token_id],
            request_id=self.token_address,
            block_id=self.block_id,
        )
        results = self.mc.agg([call])
        assert results == excepted

    def test_token_ids_do_not_match_owners(self):
        excepted = Exception(
            "the given address length does not match the length of the token id"
        )
        try:
            call = self.erc1155_service.balanceOfBatch(
                token=self.token_address,
                owners=[self.owner, self.owner],
                token_ids=[self.token_id, self.token_id, self.token_id],
                request_id=self.token_address,
                block_id=self.block_id,
            )
            self.mc.agg([call])
        except Exception as e:
            assert e.__str__() == excepted.__str__()

    def test_token_id_is_none(self):
        excepted = Exception("getting erc1155 token balance require token id")
        try:
            call = self.erc1155_service.balanceOf(
                token=self.token_address,
                owner=self.owner,
                token_id=self.token_id,
                request_id=self.token_address,
                block_id=self.block_id,
            )
            self.mc.agg([call])
        except Exception as e:
            assert e.__str__() == excepted.__str__()

    def test_get_ownerOf(self):
        excepted = [
            {
                "request_id": self.token_address,
                "result": "0x0000000000000000000000000000000000000000",
            }
        ]
        call = self.erc1155_service.ownerOf(
            token=self.token_address,
            token_id=self.token_id,
            request_id=self.token_address,
            block_id=self.block_id,
        )
        result = self.mc.agg([call])
        assert result == excepted

    def test_get_token_uri(self):
        token_address = "0xc76da013ffb85c1201523d69d300a35dae6a54f9"
        excepted = [
            {
                "request_id": token_address,
                "result": "ipfs://QmUpu4boNz21pKJcof5wfFc6Nmr1BZWMREu4Uu2VxLttsm/metadata.json",
            }
        ]
        call = self.erc1155_service.tokenURI(
            token=token_address,
            token_id=1,
            request_id=token_address,
            block_id=14201698,
        )
        result = self.mc.agg([call], ignore_error=True)
        assert result == excepted
