# Claim Check Pattern — Runnable Implementations

Companion to the StackPractices pattern [Claim Check Pattern](https://stackpractices.com/patterns/claim-check-pattern/).

A claim check demo in three equivalent implementations: an in-memory blob store simulating S3/Azure Blob/GCS, a minimal message broker, and a producer/consumer pair. The producer stores a 1MB+ report in storage, publishes only the claim token to the broker, and the consumer downloads the payload by token and deletes it after processing. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/claim_check.py` | Python 3.9+ (stdlib only) | `python src/claim_check.py` |
| `src/claim-check.js` | Node.js 14+ (stdlib only) | `node src/claim-check.js` |
| `src/ClaimCheck.java` | Java 15+ (`text blocks`, `Map.of`) | `javac src/ClaimCheck.java && java -cp src ClaimCheck` |

Each run prints the claim token, the payload size that traveled through the broker (a few hundred bytes instead of 1MB+), the retrieval and the deletion. To see the failure path, delete the token from storage before the consumer runs — the consumer logs `Claim check ... not found` instead of crashing, which is the error handling a real consumer needs.

The broker and storage here are in-memory stubs so the demo runs anywhere; in production you'd swap `BlobStorage` for an S3/Azure Blob/GCS client and `MessageBroker` for SQS, Kafka or RabbitMQ — the claim check logic stays identical.
