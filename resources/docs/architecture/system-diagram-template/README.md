# System Diagram Template — C4 Examples

Companion assets for the [System Diagram Template](https://stackpractices.com/docs/system-diagram-template/): Mermaid C4 context and container diagrams, a Structurizr DSL workspace, and a review checklist.

## Files

| File | Purpose |
|------|---------|
| `c4-context.mmd` | C4 Level 1 context diagram in Mermaid |
| `c4-container.mmd` | C4 Level 2 container diagram in Mermaid |
| `workspace.dsl` | Structurizr DSL workspace (context + container views) |
| `diagram-review-checklist.md` | Pre-merge review checklist for diagrams |

## Usage

Render the Mermaid files with mermaid-cli:

```bash
mmdc -i c4-context.mmd -o context.svg
mmdc -i c4-container.mmd -o container.svg
```

Or run Structurizr Lite for interactive C4 views:

```bash
docker run -it --rm -p 8080:8080 -v "$PWD:/usr/local/structurizr" structurizr/lite
```

Commit diagram sources (`.mmd`, `.dsl`) next to the doc — never commit only a rendered image.
