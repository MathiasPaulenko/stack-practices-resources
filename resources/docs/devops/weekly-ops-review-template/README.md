# Weekly Ops Review Template — Companion Resources

Companion files for the [Weekly Ops Review Template](https://stackpractices.com/docs/weekly-ops-review-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `weekly-ops-review.md` | Markdown | Standalone review template: executive summary, incident review, cost analysis, performance, action items, risks |
| `summarize-week.py` | Python 3 | Builds the executive summary table from a JSON export of incidents and costs; flags cost spikes and low error budgets |

## Quick start

### 1. Copy the template

```bash
cp weekly-ops-review.md reviews/$(date +%Y-%m-%d)-ops-review.md
```

### 2. Generate the summary table

```bash
python summarize-week.py week.json
```

The script reads a JSON export (`incidents`, `cost_this_week`, `cost_last_week`, `cost_budget`, `error_budget_pct`, `error_budget_last_pct`) and prints the section-1 table with week-over-week trends. Warnings appear when cost jumps >5% or error budget drops below 50%.

## Adapt before production

1. Wire the JSON export to your incident tracker and cost tool APIs.
2. Tune the targets in the table (`< 3` incidents, `> 50%` error budget) to your SLOs.
3. Keep the review under 30 minutes — the template is the agenda, not the meeting.
