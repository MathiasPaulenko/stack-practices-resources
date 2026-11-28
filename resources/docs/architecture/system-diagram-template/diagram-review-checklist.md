# Diagram Review Checklist

Run through this before merging a diagram into a design doc or RFC.

## Scope

- [ ] The diagram sits at exactly one C4 level — no containers mixed with classes
- [ ] It answers the level's key question (what is it / what are the blocks / what runs inside / how does this piece work)
- [ ] Every element fits the stated scope — nothing outside the boundary

## Notation

- [ ] Consistent shapes per element type (person, system, container, database, queue)
- [ ] Every arrow has a label saying *what* flows or *why* it exists
- [ ] Technology named on every container/component
- [ ] External systems visually distinct (grey fill or `External` tag)
- [ ] No custom icons that break in GitHub, IDE, or wiki renderers

## Readability

- [ ] Under ~15 elements per diagram; more means split it
- [ ] No crossing lines you can avoid by reordering
- [ ] Readable at 100% zoom on a laptop — not just on the author's monitor
- [ ] Alt text or surrounding prose explains the diagram for screen readers

## Maintenance

- [ ] Diagram source (`.mmd` / `.dsl`) committed next to the doc, not a binary image
- [ ] Owner and review date noted in the doc
- [ ] Level 4 diagrams generated from code, not drawn by hand
