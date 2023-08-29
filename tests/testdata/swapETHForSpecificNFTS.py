ABI_swapETHForSpecificNFTs = {
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
