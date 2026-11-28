# Thread Pool Sizing Template — Companion Resources

Companion resources for the [Thread Pool Sizing Template](https://stackpractices.com/docs/thread-pool-sizing-template/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `template.md` | Blank fillable worksheet — copy it into your service's ops docs and fill one per pool |
| `example-checkout-service.md` | Filled example: an I/O-bound checkout service calling an inventory API, numbers worked end to end |

## Usage

Copy `template.md`, measure your workload's W/C ratio under real load, and fill the placeholders. Compare against the filled example when unsure how much detail is enough — the point is a sizing decision you can defend in review, with a review date to re-measure it.
