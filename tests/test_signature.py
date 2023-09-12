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

    def test_decode_output_single_field(self):
        sig = Signature("balanceOf(address)(uint256)")
        decoded = sig.decode_data(
            "0x0000000000000000000000000000000000000000000000000000000000000001"
        )
        assert decoded == 1

    def test_decode_output_multi_fields(self):
        sig = Signature(
            "positions(uint256)(uint96,address,address,address,uint24,int24,int24,uint128,uint256,uint256,uint128,uint128)"
        )

        decoded = sig.decode_data(
            "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004200000000000000000000000000000000000006000000000000000000000000fa980ced6895ac314e7de34ef1bfae90a5add21b0000000000000000000000000000000000000000000000000000000000002710000000000000000000000000000000000000000000000000000000000000e2900000000000000000000000000000000000000000000000000000000000010d8800000000000000000000000000000000000000000000015351215ed3dfaa16c50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )

        assert len(decoded or tuple()) == len(sig.output_types)
        assert decoded == (
            0,
            "0x0000000000000000000000000000000000000000",
            "0x4200000000000000000000000000000000000006",
            "0xfa980ced6895ac314e7de34ef1bfae90a5add21b",
            10000,
            58000,
            69000,
            6259292299042925188805,
            0,
            0,
            0,
            0,
        )
