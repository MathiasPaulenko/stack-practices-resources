# Performance Budget — `<Project Name>`

## Budget Overview

| Field | Value |
|-------|-------|
| Project | Example Web App |
| Last Updated | 2026-07-05 |
| Owner | Frontend Team |
| Enforcement | CI gate + Lighthouse CI |
| Monitoring | Real User Monitoring (RUM) + Synthetic |

## 1. Route-Level Budgets

### Home Page (`/`)

| Resource Type | Budget | Current | Status | Notes |
|---------------|--------|---------|--------|-------|
| Total JS (gzipped) | 150 KB | 142 KB | ✅ | Includes vendor bundle |
| Total CSS (gzipped) | 30 KB | 28 KB | ✅ | Tailwind + custom |
| Total images | 500 KB | 480 KB | ✅ | Hero + thumbnails |
| Total fonts | 100 KB | 80 KB | ✅ | 2 font families |
| HTML | 50 KB | 35 KB | ✅ | Server-rendered |
| Total page weight | 830 KB | 765 KB | ✅ | Sum of all resources |
| JS requests | 3 | 3 | ✅ | Vendor + app + lazy |
| CSS requests | 1 | 1 | ✅ | Single stylesheet |
| Image requests | 8 | 7 | ✅ | — |
| Font requests | 2 | 2 | ✅ | — |
| Total requests | 15 | 14 | ✅ | — |

### Product Page (`/products/:id`)

| Resource Type | Budget | Current | Status | Notes |
|---------------|--------|---------|--------|-------|
| Total JS (gzipped) | 180 KB | 165 KB | ✅ | Includes product gallery |
| Total CSS (gzipped) | 35 KB | 32 KB | ✅ | — |
| Total images | 800 KB | 750 KB | ✅ | Product images |
| Total fonts | 100 KB | 80 KB | ✅ | Same as home |
| HTML | 60 KB | 42 KB | ✅ | Product data |
| Total page weight | 1,175 KB | 1,069 KB | ✅ | — |
| JS requests | 4 | 4 | ✅ | Vendor + app + gallery + reviews |
| CSS requests | 1 | 1 | ✅ | — |
| Image requests | 12 | 10 | ✅ | Gallery + thumbnails |
| Font requests | 2 | 2 | ✅ | — |
| Total requests | 20 | 18 | ✅ | — |

### Checkout Page (`/checkout`)

| Resource Type | Budget | Current | Status | Notes |
|---------------|--------|---------|--------|-------|
| Total JS (gzipped) | 200 KB | 188 KB | ✅ | Includes payment SDK |
| Total CSS (gzipped) | 35 KB | 30 KB | ✅ | — |
| Total images | 100 KB | 50 KB | ✅ | Minimal images |
| Total fonts | 100 KB | 80 KB | ✅ | — |
| HTML | 40 KB | 30 KB | ✅ | — |
| Total page weight | 475 KB | 428 KB | ✅ | — |
| JS requests | 5 | 5 | ✅ | Vendor + app + payment + validation + analytics |
| CSS requests | 1 | 1 | ✅ | — |
| Image requests | 2 | 2 | ✅ | Logo + security badge |
| Font requests | 2 | 2 | ✅ | — |
| Total requests | 11 | 11 | ✅ | — |

### Dashboard Page (`/dashboard`)

| Resource Type | Budget | Current | Status | Notes |
|---------------|--------|---------|--------|-------|
| Total JS (gzipped) | 250 KB | 245 KB | ⚠️ | Chart library is heavy |
| Total CSS (gzipped) | 40 KB | 38 KB | ✅ | — |
| Total images | 200 KB | 150 KB | ✅ | Avatars + charts |
| Total fonts | 100 KB | 80 KB | ✅ | — |
| HTML | 80 KB | 65 KB | ✅ | Dashboard data |
| Total page weight | 670 KB | 578 KB | ✅ | — |
| JS requests | 6 | 6 | ✅ | Vendor + app + charts + date + table + auth |
| CSS requests | 1 | 1 | ✅ | — |
| Image requests | 5 | 4 | ✅ | — |
| Font requests | 2 | 2 | ✅ | — |
| Total requests | 15 | 14 | ✅ | — |

## 2. Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor | Target | Current (p75) | Status |
|--------|------|-------------------|------|--------|---------------|--------|
| LCP | < 2.5s | 2.5s - 4.0s | > 4.0s | < 2.5s | 2.1s | ✅ |
| INP | < 200ms | 200ms - 500ms | > 500ms | < 200ms | 180ms | ✅ |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 | < 0.1 | 0.05 | ✅ |
| FCP | < 1.8s | 1.8s - 3.0s | > 3.0s | < 1.8s | 1.4s | ✅ |
| TTFB | < 800ms | 800ms - 1.8s | > 1.8s | < 800ms | 650ms | ✅ |

## 3. Timing Budgets

| Metric | Budget | Current | Status |
|--------|--------|---------|--------|
| Time to First Byte (TTFB) | < 800ms | 650ms | ✅ |
| First Contentful Paint (FCP) | < 1.8s | 1.4s | ✅ |
| Largest Contentful Paint (LCP) | < 2.5s | 2.1s | ✅ |
| Time to Interactive (TTI) | < 3.5s | 3.1s | ✅ |
| Total Blocking Time (TBT) | < 200ms | 150ms | ✅ |
| Cumulative Layout Shift (CLS) | < 0.1 | 0.05 | ✅ |
| Interaction to Next Paint (INP) | < 200ms | 180ms | ✅ |

## 4. Third-Party Budgets

| Third-Party | Type | JS Budget | Current | Status | Notes |
|-------------|------|-----------|---------|--------|-------|
| Google Analytics | Analytics | 45 KB | 42 KB | ✅ | Loaded async |
| Stripe.js | Payment | 50 KB | 48 KB | ✅ | Only on checkout |
| Sentry | Error tracking | 25 KB | 22 KB | ✅ | Loaded async |
| Google Maps | Maps | 80 KB | 75 KB | ✅ | Only on store locator |
| Intercom | Support | 60 KB | 55 KB | ✅ | Lazy loaded |
| **Total third-party** | | **260 KB** | **242 KB** | **✅** | |

## 5. CI Enforcement

See `ci/budget-check.yml`, `ci/check-bundle-size.js`, and `ci/lighthouserc.json` for the enforcement implementation.

## 6. Production Monitoring

### RUM Thresholds

| Metric | Alert Threshold | Page | Action |
|--------|----------------|------|--------|
| LCP p75 > 3s | Warning | Any | Investigate slow routes |
| LCP p75 > 4s | Critical | Any | Roll back if recent deploy |
| INP p75 > 300ms | Warning | Any | Check for long tasks |
| CLS p75 > 0.15 | Warning | Any | Check for layout shifts |
| TTFB p75 > 1.2s | Warning | Any | Check server response |
| JS bundle size > budget | Warning | Any | Investigate bundle growth |

### Synthetic Monitoring

| Route | Check Frequency | Metrics | Alert |
|-------|----------------|---------|-------|
| / | Every 5 min | LCP, CLS, INP, TTFB | LCP > 3s |
| /products/sample | Every 10 min | LCP, CLS, INP | LCP > 3s |
| /checkout | Every 10 min | LCP, CLS, INP | LCP > 3s |
| /dashboard | Every 10 min | LCP, CLS, INP | LCP > 3s |
