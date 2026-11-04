"""Poll the EC2 metadata service (IMDSv2) for a Spot interruption notice.

The notice arrives two minutes before termination — enough to drain
connections or checkpoint state. A 404 from spot/instance-action means
no interruption is scheduled.
"""

import json
import urllib.error
import urllib.request

METADATA = "http://169.254.169.254/latest"


def _imds(path):
    token = urllib.request.urlopen(
        urllib.request.Request(
            f"{METADATA}/api/token",
            method="PUT",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        )
    ).read()
    req = urllib.request.Request(
        f"{METADATA}/meta-data/{path}",
        headers={"X-aws-ec2-metadata-token": token},
    )
    return urllib.request.urlopen(req, timeout=1).read()


def check_spot_interruption():
    try:
        action = json.loads(_imds("spot/instance-action"))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        return
    if action["action"] == "terminate":
        graceful_shutdown()  # drain connections, persist state


def graceful_shutdown():
    raise NotImplementedError("drain connections and checkpoint state")
