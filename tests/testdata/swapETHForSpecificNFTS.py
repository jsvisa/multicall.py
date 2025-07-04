ABI_swapETHForSpecificNFTs = {
    "inputs": [
        {
            "components": [
                {"name": "pair", "type": "address"},
                {"name": "nftIds", "type": "uint256[]"},
            ],
            "name": "swapList",
            "type": "tuple[]",
        },
        {"name": "ethRecipient", "type": "address"},
        {"name": "nftRecipient", "type": "address"},
        {"name": "deadline", "type": "uint256"},
    ],
    "name": "swapETHForSpecificNFTs",
    "outputs": [{"name": "remainingValue", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function",
}
