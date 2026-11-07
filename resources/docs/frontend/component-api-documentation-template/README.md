# Component API Documentation Template — Companion Kit

Companion files for the [Component API Documentation Template](https://stackpractices.com/docs/component-api-documentation-template/) on StackPractices.

## Contents

| File | What it is |
|------|-----------|
| `component-api-doc.md` | The fillable Markdown template: overview, props table, TypeScript types, prop details, events, slots, methods, accessibility, variants, do's and don'ts, testing, migration guide. |
| `docgen_drift_check.py` | CI drift check: compares `react-docgen` output against the props documented in a Markdown file. Exits non-zero when they diverge. |
| `props-table.csv` | The Button props table as CSV — import into a spreadsheet or paste into docs that don't take Markdown tables. |
| `storybook-autodocs.mdx` | Minimal Storybook autodocs page that renders generated prop tables next to hand-written narrative. |

## Quick start

```bash
# 1. Generate docgen output for your component
npx react-docgen src/components/Button/Button.tsx --pretty > docgen.json

# 2. Fill in component-api-doc.md for the component

# 3. Verify the doc matches the code (run in CI)
python docgen_drift_check.py docgen.json component-api-doc.md
```

The drift check compares the set of prop names `react-docgen` found in the source against the prop names in the doc's `## Props` table. Any prop present in only one side fails the check — which is exactly what you want a PR to do when someone changes the component and forgets the docs.

## Notes

- `docgen_drift_check.py` reads the props table by convention: rows under `## Props` (or `## Props` translations) whose first cell is the prop name. Adjust `PROPS_HEADING` if your template uses a different heading.
- Everything is dependency-free (stdlib only for the script).
