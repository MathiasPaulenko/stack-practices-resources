# Serverless Cost Estimation: <Function / Workload Name>

Fill in every `X` and `[placeholder]` before presenting the estimate.
Reconcile against the actual bill monthly; update inputs when drift exceeds ~15%.

## 1. Function Profile

| Metric | Value | Source |
|--------|-------|--------|
| Expected invocations | X/month | [traffic forecast / analytics] |
| Average duration | X ms | [load test] |
| p99 duration | X ms | [load test] |
| Memory allocation | X MB | [power tuning result] |
| Data transfer out | X GB/month | [payload size × invocations] |
| Provisioned concurrency | X units | [latency SLA, or 0] |

## 2. Cost Breakdown

| Component | Calculation | Monthly Cost |
|-----------|-------------|--------------|
| Compute | X GB-s × $0.0000166667 | $X |
| Requests | (X - 1M) × $0.20/1M | $X |
| Provisioned concurrency | X GB-s × $0.00000497 | $X |
| Data transfer out | (X - 100) × $0.09/GB | $X |
| **Function total** | | **$X** |

## 3. Hidden Costs

| Item | Estimated | Notes |
|------|-----------|-------|
| CloudWatch Logs ingestion | $X | [KB/invocation × invocations × $0.50/GB] |
| CloudWatch Logs storage | $X | [retention days × daily GB × $0.03] |
| X-Ray tracing | $X | [sampling rate] |
| API Gateway | $X | [HTTP $1.00/1M or REST $3.50/1M] |
| Step Functions | $X | [transitions × $0.025/1K] |
| SQS / SNS / EventBridge | $X | [requests × price] |
| DynamoDB / S3 requests | $X | [per-request pricing] |
| NAT Gateway | $X | [$0.045/GB if VPC-attached] |
| **Hidden total** | **$X** | |

## 4. Scenario Summary

| Scenario | Invocations | Duration | Monthly Cost |
|----------|-------------|----------|--------------|
| Expected | X | X ms | $X |
| 3x peak | X | X ms | $X |
| 10x worst case | X | X ms | $X |

## 5. Validation Log

| Month | Estimated | Actual | Drift | Action |
|-------|-----------|--------|-------|--------|
| YYYY-MM | $X | $Y | +/- Z% | [re-estimate / tune / none] |
