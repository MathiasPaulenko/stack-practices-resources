# Capacity Planning Forecast — Companion Resources

Companion files for the [Capacity Planning Forecast Template](https://stackpractices.com/docs/capacity-planning-forecast-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `capacity-forecast-template.md` | Markdown | The fillable 9-section forecast: current state, growth assumptions, traffic projections, resource forecast, scaling plan, cost projection, risk assessment, action items, appendix |
| `capacity-dashboard-example.txt` | Text | A completed forecast rendered as a dashboard — shows how the projection flags the first bottleneck (DB connections in Oct, disk in Nov, CPU at seasonal peak) with dated actions |
| `capacity-projection.csv` | CSV | The same 6-month projection in spreadsheet form — import into Sheets/Excel and swap in your own numbers |

## Quick start

### 1. Copy the template

Drop `capacity-forecast-template.md` into your wiki or repo next to the infrastructure it describes.

### 2. Fill the current state first

Pull peak values (not averages) for the last 30 days from your monitoring stack. Agree on what "full" means per resource before projecting — 70% CPU for a database is very different from 90% on a stateless web tier.

### 3. Project and find the bottleneck

Apply your growth rate to each resource in section 4. The first resource to hit its limit sets your scaling deadline; schedule every action to land before that date minus procurement/deploy lead time.

### 4. Review quarterly

Keep dated versions of each forecast and record projected vs. actual — that folder becomes your forecasting-accuracy dataset.

## Useful formulas

- Compound monthly growth: `(end / start)^(1/months) - 1`
- Runway: `(limit - current_peak) / monthly_growth`
- Peak projection: forecast p95 busy-hour peaks, not daily averages (peak-to-average ratio is typically 1.5x–3x for web services)
