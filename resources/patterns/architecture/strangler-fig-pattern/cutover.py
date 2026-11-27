# shadow_traffic.py — send traffic to both old and new, compare results
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class ShadowTrafficRouter:
    """Send requests to both legacy and new service.
    Return the legacy response, but log differences with the new service."""

    def __init__(self, legacy_url, new_url):
        self.legacy_url = legacy_url
        self.new_url = new_url

    def route(self, method, path, headers, body, params):
        # Send to legacy (primary)
        legacy_response = requests.request(
            method=method,
            url=f"{self.legacy_url}{path}",
            headers=headers,
            data=body,
            params=params
        )

        # Shadow send to new service (don't wait for it)
        def shadow_call():
            try:
                new_response = requests.request(
                    method=method,
                    url=f"{self.new_url}{path}",
                    headers=headers,
                    data=body,
                    params=params,
                    timeout=5
                )
                self._compare(legacy_response, new_response, path)
            except Exception as e:
                logger.warning(f"Shadow call failed for {path}: {e}")

        # Run shadow call in background
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(shadow_call)

        return legacy_response

    def _compare(self, legacy_resp, new_resp, path):
        if legacy_resp.status_code != new_resp.status_code:
            logger.warning(
                f"Status mismatch for {path}: "
                f"legacy={legacy_resp.status_code}, new={new_resp.status_code}"
            )

        if legacy_resp.json() != new_resp.json():
            logger.info(f"Response body differs for {path} — investigating")
