from multicall.eth_decode import eth_decode_input


class TestEthDecode:
    def test_eth_decode_input(self):
        abi_json = {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "contract LSSVMPair",
                            "name": "pair",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256[]",
                            "name": "nftIds",
                            "type": "uint256[]",
                        },
                    ],
                    "internalType": "struct LSSVMRouter.PairSwapSpecific[]",
                    "name": "swapList",
                    "type": "tuple[]",
                },
                {
                    "internalType": "address payable",
                    "name": "ethRecipient",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "nftRecipient",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "deadline",
                    "type": "uint256",
                },
            ],
            "name": "swapETHForSpecificNFTs",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "remainingValue",
                    "type": "uint256",
                }
            ],
            "stateMutability": "payable",
            "type": "function",
        }

        data = "0x111320000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000ca6f3defbc6041299837725f6430f33b0f24e5c0000000000000000000000000ca6f3defbc6041299837725f6430f33b0f24e5c00000000000000000000000000000000000000000000000000000000062e9ca1800000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000575570f62c90a61763b1e93cf0da62ed810dbda2000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000561"  # noqa
        func_text, parameter = eth_decode_input(abi_json, data)
        WANT = "swapETHForSpecificNFTs((address,uint256[])[],address,address,uint256)"  # noqa
        assert func_text == WANT
        assert parameter == {
            "swapList": [
                {
                    "pair": "0x575570f62c90a61763b1e93cf0da62ed810dbda2",
                    "nftIds": (1377,),
                }
            ],
            "ethRecipient": "0xca6f3defbc6041299837725f6430f33b0f24e5c0",
            "nftRecipient": "0xca6f3defbc6041299837725f6430f33b0f24e5c0",
            "deadline": 1659488792,
        }
