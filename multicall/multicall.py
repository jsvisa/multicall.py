import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests.adapters
from urllib3.util.retry import Retry
from requests import Session
from typing import List, Dict, Union, Optional, Generator, Iterable, Any
from collections.abc import Sequence

from eth_utils.conversions import to_text

from .call import Call


def json_decode(json_str: str) -> Dict[Any, Any]:
    try:
        decoded = json.loads(json_str)
        return decoded
    except json.decoder.JSONDecodeError as exc:
        err_msg = f"Could not decode {json_str!r} because of {exc}."
        # Calling code may rely on catching JSONDecodeError to
        # recognize bad json so we have to re-raise the same type.
        raise json.decoder.JSONDecodeError(err_msg, exc.doc, exc.pos)


class Multicall:
    def __init__(
        self,
        provider_uri: str,
        logger: Optional[logging.Logger] = None,
        session: Optional[Session] = None,
    ):
        self.provider_uri = provider_uri
        if session is None:
            retry = Retry(
                total=3,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
                respect_retry_after_header=False,
            )
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)
            session = Session()
            session.mount("http://", adapter)
            session.mount("https://", adapter)

        self.session = session
        self.logger = logger or logging.getLogger(__name__)

    def agg(
        self,
        calls: Sequence[Call],
        as_dict: bool = False,
        ignore_error: bool = False,
        block_id: Optional[Union[str, int]] = None,
        gas_limit: Optional[int] = None,
        batch_size: int = 100,
        max_workers: int = 1,
    ) -> Union[Dict, List[Dict]]:
        assert max_workers > 0, "max_workers must be not negative"

        request_ids = set(call.request_id for call in calls)
        if len(request_ids) != len(calls):
            raise ValueError("request_id should be unique for each Call")

        id_outputs = dict()
        if max_workers == 1:
            for batch in self._partition_calls(calls, batch_size):
                outputs = self.make_batch_call(batch, block_id, gas_limit)
                id_outputs.update({e["id"]: e for e in outputs})
        else:
            with ThreadPoolExecutor(max_workers) as executor:
                futures = []
                for batch in self._partition_calls(calls, batch_size):
                    futures.append(
                        executor.submit(
                            self.make_batch_call, batch, block_id, gas_limit
                        )
                    )

                for future in as_completed(futures):
                    id_outputs.update({e["id"]: e for e in future.result()})

        if as_dict:
            return {
                c.request_id: c.decode(id_outputs[c.request_id], ignore_error)
                for c in calls
            }
        else:
            return [
                {
                    "request_id": c.request_id,
                    "result": c.decode(id_outputs[c.request_id], ignore_error),
                }
                for c in calls
            ]

    def sin(
        self,
        call: Call,
        block_id: Optional[Union[str, int]] = None,
        gas_limit: Optional[int] = None,
    ) -> Any:
        result = self.make_batch_call([call], block_id, gas_limit)[0]
        return call.decode(result)

    def make_batch_call(
        self,
        calls: List[Call],
        block_id: Optional[Union[str, int]] = None,
        gas_limit: Optional[int] = None,
    ) -> List[Dict]:
        requests = [c(block_id=block_id, gas_limit=gas_limit) for c in calls]
        outputs = self.make_batch_request(requests)
        if len(outputs) != len(requests):
            raise ValueError(
                f"multicall has {len(requests)} requests, "
                f"but got {len(outputs)} responses"
            )
        return outputs

    def make_batch_request(self, requests: List[Dict]) -> List[Dict]:
        if len(requests) == 0:
            return []

        self.logger.debug(
            "Making request HTTP. URI: %s, Request: %s",
            self.provider_uri,
            requests,
        )
        raw_response = self.session.post(
            self.provider_uri,
            json=requests if len(requests) > 1 else requests[0],
        )
        self.logger.debug(
            "Getting response HTTP. URI: %s, " "Request: %s, Response: %s",
            self.provider_uri,
            requests,
            raw_response,
        )
        text_response = to_text(text=raw_response.text)
        responses = json_decode(text_response)
        if len(requests) > 1:
            return responses  # type: ignore
        else:
            return [responses]

    def _partition_calls(
        self, calls: Iterable, batch_size: int
    ) -> Generator[List, None, None]:
        batch = []
        for item in calls:
            batch.append(item)
            if batch_size > 0 and len(batch) >= batch_size:
                yield batch
                batch = []
        if len(batch) > 0:
            yield batch
