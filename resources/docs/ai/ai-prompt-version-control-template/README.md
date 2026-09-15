# AI Prompt Version Control Template

Companion resources for the [AI Prompt Version Control Template](https://stackpractices.com/docs/ai-prompt-version-control-template/) on StackPractices.com.

## Files

| File | Purpose |
|------|---------|
| `prompt_metadata.yaml` | Example metadata file with three versions, eval scores, and rollback paths |
| `eval_prompt.py` | Evaluation script that runs a prompt version against a JSONL test set |
| `ab_test.py` | A/B testing harness that routes traffic between two prompt versions |
| `check_regression.py` | Regression check comparing old vs new eval results |
| `prompt-eval.yml` | GitHub Actions workflow for automated prompt evaluation on PR |

## Usage

1. Copy `prompt_metadata.yaml` into your prompts directory.
2. Create a `versions/` subdirectory with one `.md` file per version.
3. Create an `eval/` subdirectory with `test_set.jsonl` (200+ labeled cases).
4. Run `python eval_prompt.py --prompt prompts/classifier/prompt.md --test-set prompts/classifier/eval/test_set.jsonl --model gpt-4o-mini --threshold 0.88`.
5. Add the GitHub Actions workflow from `prompt-eval.yml` to `.github/workflows/`.

## Version Numbering

- **MAJOR**: Breaking changes (model change, output schema change, category set change). Requires re-evaluation and stakeholder approval.
- **MINOR**: Feature additions (new category, new few-shot example, system prompt restructured). Requires evaluation but not stakeholder approval.
- **PATCH**: Optimizations (token reduction, wording tweaks, formatting changes). Requires evaluation, fast approval.
