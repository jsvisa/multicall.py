from unittest.mock import MagicMock
from multicall.multicall import Multicall


def _make_mock_response(json_data):
    mock_resp = MagicMock()
    mock_resp.text = __import__("json").dumps(json_data)
    return mock_resp


def test_make_batch_request_single_error_without_id():
    """
    Some RPC nodes return an error object without an 'id' field for single
    (non-batch) requests, e.g. when rate-limiting. make_batch_request must
    inject the request id so agg() does not raise KeyError: 'id'.
    """
    mc = Multicall("http://fake-rpc")

    request = {"jsonrpc": "2.0", "id": 42, "method": "eth_call", "params": []}
    error_response = {"jsonrpc": "2.0", "error": {"code": -32007, "message": "rate limited"}}

    mc.session.post = MagicMock(return_value=_make_mock_response(error_response))

    results = mc.make_batch_request([request])

    assert len(results) == 1
    assert results[0]["id"] == 42
    assert results[0]["error"]["code"] == -32007


def test_make_batch_request_single_success():
    """Normal single request: response already has 'id', must be returned as-is."""
    mc = Multicall("http://fake-rpc")

    request = {"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": []}
    success_response = {"jsonrpc": "2.0", "id": 1, "result": "0x1234"}

    mc.session.post = MagicMock(return_value=_make_mock_response(success_response))

    results = mc.make_batch_request([request])

    assert len(results) == 1
    assert results[0]["id"] == 1
    assert results[0]["result"] == "0x1234"


def test_make_batch_request_batch_success():
    """Batch requests are returned as a list without modification."""
    mc = Multicall("http://fake-rpc")

    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": []},
        {"jsonrpc": "2.0", "id": 2, "method": "eth_call", "params": []},
    ]
    batch_response = [
        {"jsonrpc": "2.0", "id": 1, "result": "0xabc"},
        {"jsonrpc": "2.0", "id": 2, "result": "0xdef"},
    ]

    mc.session.post = MagicMock(return_value=_make_mock_response(batch_response))

    results = mc.make_batch_request(requests)

    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
