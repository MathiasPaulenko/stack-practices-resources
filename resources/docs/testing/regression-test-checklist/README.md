# Regression Test Checklist — Companion

Companion file for the [Regression Test Checklist](https://stackpractices.com/docs/regression-test-checklist/) page.

## Overview

The raw Markdown template from the page, ready to copy into your own repo. It covers pre-deploy checks (CI, code quality, environment, communication), deployment checks, post-deploy smoke tests (user journeys, API health, infrastructure, monitoring), feature-specific regression tests, rollback verification, and sign-off.

## Structure

```text
regression-test-checklist.md      # The complete template with placeholder values
regression-test-checklist.es.md   # Spanish version of the same template
```

## Usage

Copy the file into your repository (for example under `docs/` or `.github/`), replace the placeholder values (`<Release Version>`, `<Name>`, version numbers, endpoints, thresholds) with your own, and delete the sections that don't apply to your stack. Keep it in version control and update it after every incident — each incident should add a new check.
