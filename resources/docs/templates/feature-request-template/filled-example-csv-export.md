# Feature Request: CSV Export from Analytics Dashboard

## Summary
Allow users to export analytics dashboard data as CSV files.

## Problem Statement
Marketing teams need to share analytics data with stakeholders who do not have
dashboard access. Currently, they take screenshots and paste numbers into
spreadsheets manually. This happens daily across 12+ teams and takes 20-30
minutes per report. The manual process introduces transcription errors.

## Proposed Solution
Add an "Export CSV" button to each chart on the analytics dashboard. The export
should include the raw data behind the chart (not the aggregated values) with
columns for date, metric, and dimension breakdowns. Limit exports to 10,000 rows
to prevent abuse. See [File Handling](/recipes/parse-csv-files/) for
implementation patterns.

## Acceptance Criteria
- [ ] Export button appears on all chart types (line, bar, pie, table)
- [ ] CSV includes headers matching the dashboard column names
- [ ] Date range in export matches the selected dashboard filter
- [ ] Export fails gracefully if data exceeds 10,000 rows with a user-facing message
- [ ] Exported file downloads as `analytics_[chart]_[date].csv`
- [ ] Works in Chrome, Firefox, Safari, Edge

## User Value
- **Target users:** Marketing teams, account managers
- **Frequency:** Daily (12+ teams)
- **Pain level:** Annoying (20-30 min wasted per report)
- **Workaround:** Manual screenshot + spreadsheet entry (error-prone)

## Priority
- [x] High — major user pain, workaround exists but is error-prone

## Additional Context
- 3 customer accounts have specifically requested this in the last quarter
- Competitor X offers PDF export; CSV is more flexible for our users
- Estimated effort: M (2-3 sprints including QA)
- Related: a bulk export API endpoint was requested in FR-512; this covers the
  self-service UI path, and the two should be evaluated together

