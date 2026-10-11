# AI Agent Design Document — [Agent Name]

## 1. Agent Summary

```text
Agent name: [name]
Version: [X.Y.Z]
Date: [YYYY-MM-DD]
Owner: [team/person]
Status: [draft | in-review | approved | deployed]

Purpose:
  [1-2 sentence description of what the agent does]

Users:
  [Who interacts with the agent — end users, internal team, other systems]

Success criteria:
  - [measurable criterion 1]
  - [measurable criterion 2]
  - [measurable criterion 3]
```

## 2. Architecture

### 2.1 Agent Type

```text
Type: [single-agent | multi-agent | hierarchical]

Pattern:
  - ReAct (Reason + Act) — agent reasons about each step, chooses a tool, observes result
  - Plan-and-Execute — agent creates a plan, executes each step sequentially
  - Reflexion — agent evaluates its own output and retries on failure
  - Supervisor — a coordinator agent delegates to specialist sub-agents
  - Custom: [describe]
```

### 2.2 Components

```text
[Diagram or description of orchestrator, agents, tools, memory layer, output]
```

### 2.3 LLM Configuration

```yaml
llm_config:
  primary_model: "[model-id]"
  fallback_model: "[model-id]"
  temperature: 0
  max_tokens: 4096
  timeout_seconds: 30
  retry_count: 2
  retry_backoff: "exponential"
```

## 3. Tools

### 3.1 Tool Definition Format

```python
tool = {
    "name": "[tool_name]",
    "description": "[what it does, when to call it, what it returns]",
    "parameters": {"type": "object", "properties": {}, "required": []},
    "output_schema": {"type": "object", "properties": {}}
}
```

### 3.2 Tool Inventory

```text
Tool | Type | Purpose | Auth required
─────┼──────┼─────────┼──────────────
[name] | [API/Function/Webhook] | [purpose] | [auth]
```

### 3.3 Tool Selection Logic

```text
[tool_name]:
  - [when to use]
  - Trigger: "[keywords]"
```

## 4. Memory

### 4.1 Short-Term Memory

```text
Storage: [in-memory | Redis]
Retention: [session duration]
Token budget: [X tokens]
Eviction: [sliding window | summarization]
```

### 4.2 Long-Term Memory

```text
Storage: [vector DB / kv store]
Retention: [30d | 90d | permanent]
Contents: [preferences | facts | interaction summaries]
```

## 5. System Prompt

```text
You are [agent name], a [role description] for [company/product].

Your capabilities:
  - [capability]

Your tools:
  - [tool]: [one-line description]

Rules:
  1. [behavioral rule]

Response format:
  - [format per query type]
```

## 6. Safety Guardrails

### 6.1 Input Validation

```text
- Max input length: [N]
- Prompt injection detection: [method]
- Rate limiting: [N messages per window]
- Topic restriction: [restricted topics]
```

### 6.2 Output Validation

```text
- Toxicity threshold: [score]
- PII redaction: [fields]
- Hallucination check: [method]
- Response length cap: [N]
```

### 6.3 Action Guardrails

```text
Irreversible actions (require confirmation): [list]
Restricted actions (never allowed): [list]
```

## 7. Evaluation

### 7.1 Metrics

```text
Metric | Target | Measurement method
───────┼────────┼───────────────────
[metric] | [target] | [method]
```

### 7.2 Test Scenarios

```text
ID | Scenario | Expected behavior
───┼──────────┼──────────────────
T01 | [scenario] | [expected]
```

## 8. Failure Modes

```text
Failure mode | Mitigation
─────────────┼───────────
[mode] | [mitigation]
```

## 9. Deployment

```yaml
deployment:
  environment: [env]
  region: [region]

monitoring:
  log_level: [level]
  alert_webhook: "[url]"

feature_flags:
  [flag]: [true|false]
```

### Rollback Plan

```text
1. [disable mechanism]
2. [revert step]
3. [notification]
4. [postmortem step]
5. [re-deploy step]
```
