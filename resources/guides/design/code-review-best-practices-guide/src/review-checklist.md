# Code Review Checklist

Use as a floor, not a ceiling — it catches what gets missed under time pressure.

## Functionality
- [ ] Does the code do what the PR description says?
- [ ] Are edge cases handled (null, empty, boundary values)?
- [ ] Are error cases covered with appropriate handling?
- [ ] Does the code handle concurrent access if needed?

## Design
- [ ] Does the change follow existing patterns in the codebase?
- [ ] Is the change at the right level of abstraction?
- [ ] Are new dependencies justified?
- [ ] Is the change over-engineered or under-engineered?

## Readability
- [ ] Are names clear and intention-revealing?
- [ ] Are functions small and focused?
- [ ] Are comments explaining why, not what?

## Testing
- [ ] Are there tests for the new functionality?
- [ ] Do tests cover edge cases and error paths?
- [ ] Do tests run fast enough for the CI pipeline?

## Security
- [ ] Is user input validated and sanitized?
- [ ] Are secrets and credentials handled securely?
- [ ] Are permissions checked correctly?

## Performance
- [ ] Are there obvious performance issues (N+1 queries, unnecessary loops)?
- [ ] Is the change efficient for large inputs?

## Documentation
- [ ] Is the PR description clear and complete?
- [ ] Are breaking changes noted?
