from multicall.signature import Signature
from tests.testdata import ABI_swapETHForSpecificNFTs


class TestSignature:
    def test_str_signature(self):
        sig = Signature("balanceOf(address)(uint256)")
        assert sig.function == "balanceOf(address)"
        assert sig.input_types == ["address"]
        assert sig.output_types == ["uint256"]
        assert sig.fourbyte.hex() == "70a08231"

    def test_abi_signature(self):
        sig = Signature(
            {
                "name": "balanceOf",
                "inputs": [{"name": "account", "type": "address"}],
                "outputs": [{"name": "", "type": "uint256"}],
            }
        )
        assert sig.function == "balanceOf(address)"
        assert sig.input_types == ["address"]
        assert sig.output_types == ["uint256"]
        assert sig.fourbyte.hex() == "70a08231"

    def test_complex_abi_signature(self):
        sig = Signature(ABI_swapETHForSpecificNFTs)
        assert (
            sig.function
            == "swapETHForSpecificNFTs((address,uint256[])[],address,address,uint256)"
        )
        assert sig.input_types == [
            "(address,uint256[])[]",
            "address",
            "address",
            "uint256",
        ]
        assert sig.output_types == ["uint256"]
        assert sig.fourbyte.hex() == "11132000"
