ABI_matchAdvancedOrders = {
    "name": "matchAdvancedOrders",
    "type": "function",
    "inputs": [
        {
            "name": "orders",
            "type": "tuple[]",
            "components": [
                {
                    "name": "parameters",
                    "type": "tuple",
                    "components": [
                        {
                            "name": "offerer",
                            "type": "address",
                            "internalType": "address",
                        },
                        {"name": "zone", "type": "address", "internalType": "address"},
                        {
                            "name": "offer",
                            "type": "tuple[]",
                            "components": [
                                {
                                    "name": "itemType",
                                    "type": "uint8",
                                    "internalType": "enumItemType",
                                },
                                {
                                    "name": "token",
                                    "type": "address",
                                    "internalType": "address",
                                },
                                {
                                    "name": "identifierOrCriteria",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "startAmount",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "endAmount",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                            ],
                            "internalType": "structOfferItem[]",
                        },
                        {
                            "name": "consideration",
                            "type": "tuple[]",
                            "components": [
                                {
                                    "name": "itemType",
                                    "type": "uint8",
                                    "internalType": "enumItemType",
                                },
                                {
                                    "name": "token",
                                    "type": "address",
                                    "internalType": "address",
                                },
                                {
                                    "name": "identifierOrCriteria",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "startAmount",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "endAmount",
                                    "type": "uint256",
                                    "internalType": "uint256",
                                },
                                {
                                    "name": "recipient",
                                    "type": "address",
                                    "internalType": "addresspayable",
                                },
                            ],
                            "internalType": "structConsiderationItem[]",
                        },
                        {
                            "name": "orderType",
                            "type": "uint8",
                            "internalType": "enumOrderType",
                        },
                        {
                            "name": "startTime",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "endTime",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "zoneHash",
                            "type": "bytes32",
                            "internalType": "bytes32",
                        },
                        {"name": "salt", "type": "uint256", "internalType": "uint256"},
                        {
                            "name": "conduitKey",
                            "type": "bytes32",
                            "internalType": "bytes32",
                        },
                        {
                            "name": "totalOriginalConsiderationItems",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                    ],
                    "internalType": "structOrderParameters",
                },
                {"name": "numerator", "type": "uint120", "internalType": "uint120"},
                {"name": "denominator", "type": "uint120", "internalType": "uint120"},
                {"name": "signature", "type": "bytes", "internalType": "bytes"},
                {"name": "extraData", "type": "bytes", "internalType": "bytes"},
            ],
            "internalType": "structAdvancedOrder[]",
        },
        {
            "name": "criteriaResolvers",
            "type": "tuple[]",
            "components": [
                {"name": "orderIndex", "type": "uint256", "internalType": "uint256"},
                {"name": "side", "type": "uint8", "internalType": "enumSide"},
                {"name": "index", "type": "uint256", "internalType": "uint256"},
                {"name": "identifier", "type": "uint256", "internalType": "uint256"},
                {
                    "name": "criteriaProof",
                    "type": "bytes32[]",
                    "internalType": "bytes32[]",
                },
            ],
            "internalType": "structCriteriaResolver[]",
        },
        {
            "name": "fulfillments",
            "type": "tuple[]",
            "components": [
                {
                    "name": "offerComponents",
                    "type": "tuple[]",
                    "components": [
                        {
                            "name": "orderIndex",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "itemIndex",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                    ],
                    "internalType": "structFulfillmentComponent[]",
                },
                {
                    "name": "considerationComponents",
                    "type": "tuple[]",
                    "components": [
                        {
                            "name": "orderIndex",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "itemIndex",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                    ],
                    "internalType": "structFulfillmentComponent[]",
                },
            ],
            "internalType": "structFulfillment[]",
        },
        {"name": "recipient", "type": "address", "internalType": "address"},
    ],
    "outputs": [
        {
            "name": "executions",
            "type": "tuple[]",
            "components": [
                {
                    "name": "item",
                    "type": "tuple",
                    "components": [
                        {
                            "name": "itemType",
                            "type": "uint8",
                            "internalType": "enumItemType",
                        },
                        {"name": "token", "type": "address", "internalType": "address"},
                        {
                            "name": "identifier",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "amount",
                            "type": "uint256",
                            "internalType": "uint256",
                        },
                        {
                            "name": "recipient",
                            "type": "address",
                            "internalType": "addresspayable",
                        },
                    ],
                    "internalType": "structReceivedItem",
                },
                {"name": "offerer", "type": "address", "internalType": "address"},
                {"name": "conduitKey", "type": "bytes32", "internalType": "bytes32"},
            ],
            "internalType": "structExecution[]",
        }
    ],
    "stateMutability": "payable",
}
