# AI Agent Design Document — OrderBot

Filled example of the [AI agent design document template](https://stackpractices.com/docs/ai-agent-design-document-template/) for a fictional e-commerce support agent.

## 1. Agent Summary

```text
Agent name: OrderBot
Version: 1.2.0
Date: 2026-10-11
Owner: Support Platform Team / M. Paulenko
Status: deployed

Purpose:
  Resolves order-status, return-policy, and shipping queries for the
  storefront without human involvement; escalates billing disputes.

Users:
  End customers on web chat and the mobile app.

Success criteria:
  - Resolve >= 85% of conversations without escalation
  - CSAT >= 4.0/5 on post-conversation survey
  - Cost per conversation < $0.10
```

## 2. Architecture

### 2.1 Agent Type

```text
Type: single-agent

Pattern: ReAct — the agent reasons per turn, picks one tool, observes
the result. A supervisor was considered and rejected: only one domain
(order support), so routing added latency with no benefit.
```

### 2.3 LLM Configuration

```yaml
llm_config:
  primary_model: "gpt-4o"
  fallback_model: "claude-sonnet-4-5"
  temperature: 0
  max_tokens: 2048
  timeout_seconds: 30
  retry_count: 2
  retry_backoff: "exponential"
```

## 3. Tools

```text
Tool              | Type    | Purpose                    | Auth required
──────────────────┼─────────┼────────────────────────────┼──────────────
get_order_status  | API     | Fetch order tracking info  | OAuth token
get_return_policy | Function| Return policy per category | None
create_return     | API     | Start a return request     | OAuth token
escalate_to_human | Webhook | Notify support team        | Webhook secret
```

```text
escalate_to_human:
  - Billing dispute or complaint
  - User asks for a human twice
  - 3 failed resolution attempts
```

## 4. Memory

```text
Short-term: Redis session store, 20-message sliding window,
  summarize when > 8k tokens.
Long-term: pgvector — stores opted-in preferences only
  (locale, notification channel). 90-day retention.
```

## 5. System Prompt (excerpt)

```text
You are OrderBot, a customer support agent for [Storefront].
Never guess order data — always call get_order_status.
Confirm before create_return; a return is irreversible.
```

## 6. Safety Guardrails

```text
Input: 5k char cap, injection classifier, 20 msg/min rate limit.
Output: toxicity > 0.7 rejected, PII redacted, 2k char cap.
Actions: create_return requires confirmation; refunds are never
  processed by the agent (human only).
```

## 7. Evaluation

```text
Task completion rate   | > 85%  | unescalated conversations
Tool call accuracy     | > 90%  | sampled weekly by review
Hallucination rate     | < 5%   | claims checked vs tool output
Escalation rate        | < 15%  | conversations escalated
```

## 8. Failure Modes (top 3)

```text
LLM timeout            | retry 2x, fallback model, apologize
Tool returns bad data  | schema-validate, escalate
Injection attempt      | reject, log, continue normally
```

## 9. Deployment

```yaml
feature_flags:
  enable_create_return: true
  enable_long_term_memory: false  # pending privacy review
```

Rollback: disable `agent_enabled` flag — traffic routes to the
human queue. Postmortem within 48h for any user-facing incident.
