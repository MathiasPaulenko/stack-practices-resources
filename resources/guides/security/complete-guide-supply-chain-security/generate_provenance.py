"""Generate a SLSA v1.0 provenance attestation (in-toto statement).

Usage:
    python generate_provenance.py
"""
import json
from datetime import datetime, timezone


def generate_provenance(
    source_repo: str,
    commit_sha: str,
    build_command: str,
    artifacts: list,
    builder_id: str,
) -> dict:
    """Generate a SLSA v1.0 provenance attestation (in-toto statement)."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [
            {
                "name": artifact["name"],
                "digest": artifact["digest"],
            }
            for artifact in artifacts
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://github.com/myorg/myrepo/.github/workflows/build.yml",
                "externalParameters": {
                    "repository": source_repo,
                    "ref": commit_sha,
                    "command": build_command,
                },
                "internalParameters": {},
                "resolvedDependencies": [
                    {
                        "uri": source_repo,
                        "digest": {"gitCommit": commit_sha},
                    }
                ],
            },
            "runDetails": {
                "builder": {"id": builder_id},
                "metadata": {
                    "startedOn": now,
                    "finishedOn": now,
                    "invocationId": f"{source_repo}/actions/runs/1",
                },
            },
        },
    }


if __name__ == "__main__":
    provenance = generate_provenance(
        source_repo="https://github.com/myorg/myapp",
        commit_sha="abc123def456",
        build_command="docker build -t myapp:v1.0.0 .",
        artifacts=[{
            "name": "ghcr.io/myorg/myapp:v1.0.0",
            "digest": {"sha256": "a1b2c3d4e5f6..."},
        }],
        builder_id="https://github.com/actions/runner",
    )

    with open("provenance.json", "w") as f:
        json.dump(provenance, f, indent=2)
    print("Wrote provenance.json")
