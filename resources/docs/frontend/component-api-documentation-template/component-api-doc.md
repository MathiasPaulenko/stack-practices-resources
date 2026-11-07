# Component API — `<[ComponentName]>`

## Component Overview

| Field | Value |
|-------|-------|
| Component Name | [ComponentName] |
| Package | [npm package, e.g. @acme/ui] |
| Version | [semver] |
| Status | [Draft / Beta / Stable / Deprecated] |
| Last Updated | [YYYY-MM-DD] |
| Maintainer | [team or owner] |
| Source | [path in repo] |
| Bundle Size (gzipped) | [size] |
| Dependencies | [runtime deps or "none"] |

## Description

[2–3 sentences: what the component does, the main variants or states, and how it renders by default.]

## Installation

```bash
npm install [package]
```

## Basic Usage

```tsx
import { [ComponentName] } from '[package]';

function Example() {
  return <[ComponentName]>[minimal working usage]</[ComponentName]>;
}
```

## Props

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| [propName] | [type or union] | [default] | [Yes/No] | [what it controls] |

### TypeScript Types

```typescript
interface [ComponentName]Props {
  // paste the public interface here
}
```

### Prop Details

#### `[propName]`

[Paragraph: what it controls, interaction with other props, edge cases.]

```tsx
[one example per meaningful value]
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `[eventName]` | `[payload type]` | [when it fires — including when it does NOT fire] |

### Event Examples

```tsx
[handler example showing async or edge-case usage]
```

## Slots

| Slot | Default | Description |
|------|---------|-------------|
| `[slotName]` | [default] | [what content is expected and where it renders] |

## Methods

[Imperative methods exposed via ref, or one line stating none are exposed.]

## Accessibility

| Attribute | Value | Notes |
|-----------|-------|-------|
| Role | `[role]` | [native element or ARIA role] |
| Keyboard | [keys] | [what each key does] |
| Focus | [behavior] | [focus-visible, trapping, etc.] |
| Label | `aria-label` | [when it's required] |

## Do's and Don'ts

| Do | Don't |
|----|-------|
| [recommended usage] | [the misuse it prevents] |

## Testing

```tsx
[key behaviors as executable tests: render, events, disabled/edge states, a11y roles]
```

## Migration Guide

### [vOld] to [vNew]

| Old API | New API | Breaking Change |
|---------|---------|-----------------|
| [old prop] | [new prop] | [why it changed] |
