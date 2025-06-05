ABI_smartSwapByOrderId = {
    "name": "smartSwapByOrderId",
    "type": "function",
    "inputs": [
        {"name": "orderId", "type": "uint256", "internalType": "uint256"},
        {
            "name": "baseRequest",
            "type": "tuple",
            "components": [
                {"name": "fromToken", "type": "uint256", "internalType": "uint256"},
                {"name": "toToken", "type": "address", "internalType": "address"},
                {
                    "name": "fromTokenAmount",
                    "type": "uint256",
                    "internalType": "uint256",
                },
                {
                    "name": "minReturnAmount",
                    "type": "uint256",
                    "internalType": "uint256",
                },
                {"name": "deadLine", "type": "uint256", "internalType": "uint256"},
            ],
            "internalType": "struct DexRouter.BaseRequest",
        },
        {"name": "batchesAmount", "type": "uint256[]", "internalType": "uint256[]"},
        {
            "name": "batches",
            "type": "tuple[][]",
            "components": [
                {
                    "name": "mixAdapters",
                    "type": "address[]",
                    "internalType": "address[]",
                },
                {"name": "assetTo", "type": "address[]", "internalType": "address[]"},
                {"name": "rawData", "type": "uint256[]", "internalType": "uint256[]"},
                {"name": "extraData", "type": "bytes[]", "internalType": "bytes[]"},
                {"name": "fromToken", "type": "uint256", "internalType": "uint256"},
            ],
            "internalType": "struct DexRouter.RouterPath[][]",
        },
        {
            "name": "extraData",
            "type": "tuple[]",
            "components": [
                {"name": "pathIndex", "type": "uint256", "internalType": "uint256"},
                {"name": "payer", "type": "address", "internalType": "address"},
                {"name": "fromToken", "type": "address", "internalType": "address"},
                {"name": "toToken", "type": "address", "internalType": "address"},
                {
                    "name": "fromTokenAmountMax",
                    "type": "uint256",
                    "internalType": "uint256",
                },
                {
                    "name": "toTokenAmountMax",
                    "type": "uint256",
                    "internalType": "uint256",
                },
                {"name": "salt", "type": "uint256", "internalType": "uint256"},
                {"name": "deadLine", "type": "uint256", "internalType": "uint256"},
                {"name": "isPushOrder", "type": "bool", "internalType": "bool"},
                {"name": "extension", "type": "bytes", "internalType": "bytes"},
            ],
            "internalType": "struct PMMLib.PMMSwapRequest[]",
        },
    ],
    "outputs": [{"name": "returnAmount", "type": "uint256", "internalType": "uint256"}],
    "stateMutability": "payable",
}
