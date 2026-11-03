# Review Comment Examples — BAD vs GOOD

## Focus on the code, not the person

```markdown
# BAD: personal attack
"Why did you do it this way? This is obviously wrong."

# GOOD: focuses on the code
"This approach has a potential issue with concurrent access.
Consider using a mutex here. What do you think?"
```

## Ask, don't order

```markdown
# BAD: dictatorial
"Change this to use a Map instead."

# GOOD: collaborative question
"Would a Map be more efficient here? The current approach
iterates the array on every lookup, which could be slow
with large datasets."
```

## Be specific

```markdown
# BAD: vague
"This code is messy."

# GOOD: specific and actionable
"The `processData` function handles validation, transformation,
and database insertion. Extracting the validation into a
separate function would make each responsibility clearer
and easier to test."
```
