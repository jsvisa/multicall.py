ABI_swapExactTokenForPt = {
    "inputs": [
        {"internalType": "address", "name": "receiver", "type": "address"},
        {"internalType": "address", "name": "market", "type": "address"},
        {"internalType": "uint256", "name": "minPtOut", "type": "uint256"},
        {
            "components": [
                {"internalType": "uint256", "name": "guessMin", "type": "uint256"},
                {"internalType": "uint256", "name": "guessMax", "type": "uint256"},
                {"internalType": "uint256", "name": "guessOffchain", "type": "uint256"},
                {"internalType": "uint256", "name": "maxIteration", "type": "uint256"},
                {"internalType": "uint256", "name": "eps", "type": "uint256"},
            ],
            "internalType": "struct ApproxParams",
            "name": "guessPtOut",
            "type": "tuple",
        },
        {
            "components": [
                {"internalType": "address", "name": "tokenIn", "type": "address"},
                {"internalType": "uint256", "name": "netTokenIn", "type": "uint256"},
                {"internalType": "address", "name": "tokenMintSy", "type": "address"},
                {"internalType": "address", "name": "pendleSwap", "type": "address"},
                {
                    "components": [
                        {
                            "internalType": "enum SwapType",
                            "name": "swapType",
                            "type": "uint8",
                        },
                        {
                            "internalType": "address",
                            "name": "extRouter",
                            "type": "address",
                        },
                        {
                            "internalType": "bytes",
                            "name": "extCalldata",
                            "type": "bytes",
                        },
                        {"internalType": "bool", "name": "needScale", "type": "bool"},
                    ],
                    "internalType": "struct SwapData",
                    "name": "swapData",
                    "type": "tuple",
                },
            ],
            "internalType": "struct TokenInput",
            "name": "input",
            "type": "tuple",
        },
        {
            "components": [
                {"internalType": "address", "name": "limitRouter", "type": "address"},
                {"internalType": "uint256", "name": "epsSkipMarket", "type": "uint256"},
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint256",
                                    "name": "salt",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "expiry",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "nonce",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "enum OrderType",
                                    "name": "orderType",
                                    "type": "uint8",
                                },
                                {
                                    "internalType": "address",
                                    "name": "token",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "YT",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "maker",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "receiver",
                                    "type": "address",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "makingAmount",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "lnImpliedRate",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "failSafeRate",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "permit",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct Order",
                            "name": "order",
                            "type": "tuple",
                        },
                        {"internalType": "bytes", "name": "signature", "type": "bytes"},
                        {
                            "internalType": "uint256",
                            "name": "makingAmount",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct FillOrderParams[]",
                    "name": "normalFills",
                    "type": "tuple[]",
                },
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint256",
                                    "name": "salt",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "expiry",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "nonce",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "enum OrderType",
                                    "name": "orderType",
                                    "type": "uint8",
                                },
                                {
                                    "internalType": "address",
                                    "name": "token",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "YT",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "maker",
                                    "type": "address",
                                },
                                {
                                    "internalType": "address",
                                    "name": "receiver",
                                    "type": "address",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "makingAmount",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "lnImpliedRate",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "failSafeRate",
                                    "type": "uint256",
                                },
                                {
                                    "internalType": "bytes",
                                    "name": "permit",
                                    "type": "bytes",
                                },
                            ],
                            "internalType": "struct Order",
                            "name": "order",
                            "type": "tuple",
                        },
                        {"internalType": "bytes", "name": "signature", "type": "bytes"},
                        {
                            "internalType": "uint256",
                            "name": "makingAmount",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct FillOrderParams[]",
                    "name": "flashFills",
                    "type": "tuple[]",
                },
                {"internalType": "bytes", "name": "optData", "type": "bytes"},
            ],
            "internalType": "struct LimitOrderData",
            "name": "",
            "type": "tuple",
        },
    ],
    "name": "swapExactTokenForPt",
    "outputs": [
        {"internalType": "uint256", "name": "tokensToEnable", "type": "uint256"},
        {"internalType": "uint256", "name": "tokensToDisable", "type": "uint256"},
    ],
    "stateMutability": "nonpayable",
    "type": "function",
}
