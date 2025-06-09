ABI_swapETHForSpecificNFTs_noName = {
    "inputs": [
        {
            "components": [
                {"name": "", "type": "address"},
                {"name": "", "type": "uint256[]"},
            ],
            "name": "swapList",
            "type": "tuple[]",
        },
        {"name": "", "type": "address"},
        {"name": "nftRecipient", "type": "address"},
        {"name": "", "type": "uint256"},
    ],
    "name": "swapETHForSpecificNFTs",
    "outputs": [{"name": "remainingValue", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function",
}
