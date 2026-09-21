# Onboarding Checklist — Frontend / QA Variants

Diff-only adaptations of the main checklist. Everything not listed here stays identical.

## Frontend Engineer

### Day 1 — Development Environment (replaces backend items)
- [ ] Node.js / package manager (npm / pnpm / yarn) with team version
- [ ] Browser dev tools configured (React/Vue devtools, accessibility inspector)
- [ ] Design tool access (Figma / Storybook)
- [ ] Component library and design system repos cloned
- [ ] Local dev server + hot reload verified

### Week 1 — replaces "Architecture and Systems" additions
- [ ] Understand the rendering model (SSR / CSR / SSG) and routing
- [ ] Review the design system: tokens, components, usage rules
- [ ] Run the accessibility audit flow (axe, keyboard nav, screen reader basics)
- [ ] Review browser support matrix and testing matrix
- [ ] Understand the build pipeline (Vite / webpack / bundler config)

### Week 2 — replaces "Production Awareness" additions
- [ ] Review Core Web Vitals dashboards and performance budgets
- [ ] Understand feature flags and A/B test tooling
- [ ] Review error monitoring (Sentry / equivalent) for frontend sessions
- [ ] Cross-browser smoke test on the testing matrix browsers

## QA Engineer

### Day 1 — Development Environment additions
- [ ] Test framework setup (Playwright / Cypress / equivalent)
- [ ] Test management tool access (TestRail / Xray / equivalent)
- [ ] Staging and ephemeral environment access

### Week 1 — replaces "Code Standards" additions
- [ ] Review test pyramid and coverage expectations
- [ ] Read 5 recently filed bugs to understand report quality bar
- [ ] Run the existing e2e suite locally and in CI
- [ ] Understand the release checklist and sign-off process

### Week 2 — replaces "Domain Knowledge" additions
- [ ] Review the flaky-test backlog and quarantine process
- [ ] Pair with a developer on a bug reproduction
- [ ] Write first automated test for a real feature
- [ ] Review regression suite ownership and rotation
