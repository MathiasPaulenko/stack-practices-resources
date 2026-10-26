# Accessibility Audit Checklist — `<Project Name>`

## Audit Information

| Field | Value |
|-------|-------|
| Project | <Project Name> |
| Auditor | <Name> |
| Date | <YYYY-MM-DD> |
| WCAG Version | 2.2 |
| Conformance Target | AA |
| Pages Audited |  |
| Total Criteria | 86 |
| Passed |  |
| Failed |  |
| Not Applicable |  |

## Testing Tools

| Tool | Type | Purpose |
|------|------|---------|
| axe DevTools | Automated | Browser extension for automated scans |
| Lighthouse | Automated | Chrome DevTools accessibility audit |
| WAVE | Automated | Web accessibility evaluation tool |
| NVDA | Screen reader | Windows screen reader testing |
| VoiceOver | Screen reader | macOS/iOS screen reader testing |
| Keyboard only | Manual | Tab navigation testing |
| Colour Contrast Analyser | Manual | Color contrast verification |
| W3C Validator | Automated | HTML validation |

## 1. Perceivable (WCAG 2.2)

### 1.1 Text Alternatives

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 1.1.1 Non-text Content | A |  |  |  |
| Images with text | — |  |  |  |
| Complex images | — |  |  |  |
| CAPTCHA | — |  |  |  |

### 1.2 Time-based Media

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 1.2.1 Audio-only and Video-only | A |  |  |  |
| 1.2.2 Captions (Prerecorded) | A |  |  |  |
| 1.2.3 Audio Description or Media Alternative | A |  |  |  |
| 1.2.4 Captions (Live) | AA |  |  |  |
| 1.2.5 Audio Description (Prerecorded) | AA |  |  |  |
| 1.2.6 Sign Language | AAA |  |  |  |
| 1.2.7 Extended Audio Description | AAA |  |  |  |
| 1.2.8 Media Alternative | AAA |  |  |  |
| 1.2.9 Audio-only (Live) | AAA |  |  |  |

### 1.3 Adaptable

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 1.3.1 Info and Relationships | A |  |  |  |
| 1.3.2 Meaningful Sequence | A |  |  |  |
| 1.3.3 Sensory Characteristics | A |  |  |  |
| 1.3.4 Orientation | AA |  |  |  |
| 1.3.5 Identify Input Purpose | AA |  |  |  |
| 1.3.6 Identify Purpose | AAA |  |  |  |

### 1.4 Distinguishable

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 1.4.1 Use of Color | A |  |  |  |
| 1.4.2 Audio Control | A |  |  |  |
| 1.4.3 Contrast (Minimum) | AA |  |  |  |
| 1.4.4 Resize Text | AA |  |  |  |
| 1.4.5 Images of Text | A |  |  |  |
| 1.4.6 Contrast (Enhanced) | AAA |  |  |  |
| 1.4.7 Low or No Background Audio | AAA |  |  |  |
| 1.4.8 Visual Presentation | AAA |  |  |  |
| 1.4.9 Images of Text (No Exception) | AAA |  |  |  |
| 1.4.10 Reflow | AA |  |  |  |
| 1.4.11 Non-text Contrast | AA |  |  |  |
| 1.4.12 Text Spacing | AA |  |  |  |
| 1.4.13 Content on Hover or Focus | A |  |  |  |

## 2. Operable (WCAG 2.2)

### 2.1 Keyboard Accessible

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 2.1.1 Keyboard | A |  |  |  |
| 2.1.2 No Keyboard Trap | A |  |  |  |
| 2.1.3 Keyboard (No Exception) | AAA |  |  |  |
| 2.1.4 Character Key Shortcuts | A |  |  |  |

### 2.2 Enough Time

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 2.2.1 Timing Adjustable | A |  |  |  |
| 2.2.2 Pause, Stop, Hide | A |  |  |  |
| 2.2.3 No Timing | AAA |  |  |  |
| 2.2.4 Interruptions | AAA |  |  |  |
| 2.2.5 Re-authenticating | AAA |  |  |  |
| 2.2.6 Timeouts | AAA |  |  |  |

### 2.3 Seizures and Physical Reactions

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 2.3.1 Three Flashes or Below | A |  |  |  |
| 2.3.2 Three Flashes | AAA |  |  |  |
| 2.3.3 Animation from Interactions | AAA |  |  |  |

### 2.4 Navigable

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 2.4.1 Bypass Blocks | A |  |  |  |
| 2.4.2 Page Titled | A |  |  |  |
| 2.4.3 Focus Order | A |  |  |  |
| 2.4.4 Link Purpose (In Context) | A |  |  |  |
| 2.4.5 Multiple Ways | AA |  |  |  |
| 2.4.6 Headings and Labels | AA |  |  |  |
| 2.4.7 Focus Visible | AA |  |  |  |
| 2.4.8 Location | AAA |  |  |  |
| 2.4.9 Link Purpose (Link Only) | AAA |  |  |  |
| 2.4.10 Section Headings | AAA |  |  |  |
| 2.4.11 Focus Not Obscured (Minimum) | AA |  |  |  |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA |  |  |  |
| 2.4.13 Focus Appearance | AAA |  |  |  |

### 2.5 Input Modalities

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 2.5.1 Pointer Gestures | A |  |  |  |
| 2.5.2 Pointer Cancellation | A |  |  |  |
| 2.5.3 Label in Name | A |  |  |  |
| 2.5.4 Motion Actuation | A |  |  |  |
| 2.5.5 Target Size (Enhanced) | AAA |  |  |  |
| 2.5.6 Concurrent Input Mechanisms | AAA |  |  |  |
| 2.5.7 Dragging Movements | AA |  |  |  |
| 2.5.8 Target Size (Minimum) | AA |  |  |  |

## 3. Understandable (WCAG 2.2)

### 3.1 Readable

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 3.1.1 Language of Page | A |  |  |  |
| 3.1.2 Language of Parts | AA |  |  |  |
| 3.1.3 Unusual Words | AAA |  |  |  |
| 3.1.4 Abbreviations | AAA |  |  |  |
| 3.1.5 Reading Level | AAA |  |  |  |
| 3.1.6 Pronunciation | AAA |  |  |  |

### 3.2 Predictable

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 3.2.1 On Focus | A |  |  |  |
| 3.2.2 On Input | A |  |  |  |
| 3.2.3 Consistent Navigation | AA |  |  |  |
| 3.2.4 Consistent Identification | AA |  |  |  |
| 3.2.5 Change on Request | AAA |  |  |  |
| 3.2.6 Consistent Help | A |  |  |  |

### 3.3 Input Assistance

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 3.3.1 Error Identification | A |  |  |  |
| 3.3.2 Labels or Instructions | A |  |  |  |
| 3.3.3 Error Suggestion | AA |  |  |  |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA |  |  |  |
| 3.3.5 Help | AAA |  |  |  |
| 3.3.6 Error Prevention (All) | AAA |  |  |  |
| 3.3.7 Redundant Entry | A |  |  |  |
| 3.3.8 Accessible Authentication (Minimum) | AA |  |  |  |

## 4. Robust (WCAG 2.2)

### 4.1 Compatible

| Criterion | Level | Status | Test Method | Notes |
|-----------|-------|--------|-------------|-------|
| 4.1.1 Parsing | A |  |  |  |
| 4.1.2 Name, Role, Value | A |  |  |  |
| 4.1.3 Status Messages | AA |  |  |  |

## 5. Failed Criteria Summary

| # | Criterion | Severity | Page | Issue | Remediation | Effort |
|---|-----------|----------|------|-------|-------------|--------|
| 1 | 1.3.1 Info and Relationships | High | Checkout | Form labels not associated with inputs via for/id | Add for/id association | 2h |
| 2 | 1.4.3 Contrast (Minimum) | Medium | Global | Gray text (#999) on white = 2.8:1 ratio | Change to #767676 (4.5:1) | 1h |
| 3 | 1.4.11 Non-text Contrast | Medium | Global | UI borders (#ddd) on white = 1.4:1 ratio | Change to #949494 (3:1) | 1h |
| 4 | 2.4.3 Focus Order | High | Modals | Focus trapped in modal, not returning to trigger | Implement focus management in modal | 4h |
| 5 | 2.4.6 Headings and Labels | Medium | Dashboard | Section headings missing on data tables | Add h3 headings per section | 2h |
| 6 | 2.5.3 Label in Name | Medium | Global | Icon-only buttons lack aria-label | Add aria-label to icon buttons | 2h |
| 7 | 2.5.8 Target Size (Minimum) | Low | Blog | Inline text links < 24px height | Add padding to links | 1h |
| 8 | 3.3.1 Error Identification | High | Forms | Errors shown visually but not announced | Add aria-live + role=alert to error regions | 3h |
| 9 | 3.3.2 Labels or Instructions | Medium | Search | Search input has placeholder but no label | Add visually-hidden label | 1h |
| 10 | 4.1.2 Name, Role, Value | High | Custom tabs | Tab widget missing ARIA roles | Add role=tablist, role=tab, aria-selected | 4h |
| 11 | 4.1.3 Status Messages | Medium | Global | Toast notifications not announced | Add aria-live=polite to toast container | 2h |

## 6. Remediation Plan

| Priority | Criteria | Effort | Owner | Due Date |
|----------|----------|--------|-------|----------|
| P1 | #1, #4, #8, #10 | 13h | Frontend team | 2026-07-12 |
| P2 | #2, #3, #5, #6, #9, #11 | 9h | Frontend team | 2026-07-19 |
| P3 | #7 | 1h | Frontend team | 2026-07-26 |
