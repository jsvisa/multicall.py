ABI_updateDepositTree = {
    "name": "updateDepositTree",
    "type": "function",
    "inputs": [
        {"name": "_proof", "type": "bytes", "internalType": "bytes"},
        {"name": "_argsHash", "type": "bytes32", "internalType": "bytes32"},
        {"name": "_currentRoot", "type": "bytes32", "internalType": "bytes32"},
        {"name": "_newRoot", "type": "bytes32", "internalType": "bytes32"},
        {"name": "_pathIndices", "type": "uint32", "internalType": "uint32"},
        {
            "name": "_events",
            "type": "tuple[256]",
            "components": [
                {"name": "hash", "type": "bytes32", "internalType": "bytes32"},
                {"name": "instance", "type": "address", "internalType": "address"},
                {"name": "block", "type": "uint32", "internalType": "uint32"},
            ],
            "internalType": "struct TornadoTrees.TreeLeaf[256]",
        },
    ],
    "outputs": [],
    "stateMutability": "nonpayable",
}
