"""LaunchDarkly managed feature flag client example.

Requires: pip install ldclient
Set env: LAUNCHDARKLY_SDK_KEY
"""

import os

from ldclient import LDClient
from ldclient.config import Config

ldclient = LDClient(Config(sdk_key=os.environ.get("LAUNCHDARKLY_SDK_KEY", "")))


def is_enabled(flag: str, user: dict) -> bool:
    return ldclient.variation(flag, user, default=False)


if __name__ == "__main__":
    user = {"key": "user_123", "email": "user@example.com", "country": "US"}
    if is_enabled("new_checkout", user):
        print("Rendering new checkout")
    else:
        print("Rendering old checkout")
