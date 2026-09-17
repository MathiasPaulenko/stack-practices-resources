# Few-Shot Prompt Template

Reusable skeleton for classification/extraction prompts. Keep examples consistent:
same fields, same order, same formatting — mixed formats teach the model noise.

```text
SYSTEM:
Classify <thing> into exactly one of: <LABEL_A>, <LABEL_B>, <LABEL_C>, or <LABEL_D>.
Respond with the label only — no explanation.

FEW-SHOT EXAMPLES (user/assistant pairs):

user: <example input 1 — a typical case>
assistant: <LABEL_A>

user: <example input 2 — a different typical case>
assistant: <LABEL_B>

user: <example input 3 — an edge case or ambiguous phrasing>
assistant: <LABEL_C>

user: <example input 4 — the boundary between two labels>
assistant: <LABEL_D>

RUNTIME:
user: {{user_input}}
```

## Checklist

- 3–5 examples beat 10 mediocre ones.
- Include at least one edge case and one boundary case.
- Use `temperature=0` for classification/extraction tasks.
- Keep the label vocabulary closed — never let the model invent labels.
- If examples get ignored, check formatting consistency first.
