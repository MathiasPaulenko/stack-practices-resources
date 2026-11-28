# Threat Modeling Session Worksheet

Service/system: ______________  Date: ______  Facilitator: ______________
Attendees: ______________  Duration: 90–120 min

## 1. Data Flow Diagram checklist

- [ ] External entities drawn (users, browsers, third-party systems)
- [ ] Processes drawn (services, functions, jobs)
- [ ] Data stores drawn (databases, caches, queues, file systems)
- [ ] Data flows labeled with protocol (HTTP, gRPC, queue, internal call)
- [ ] Trust boundaries marked (public internet → VPC, user input → parser, service A → service B)

## 2. STRIDE pass — one row per plausible threat

| Element | Category (S/T/R/I/D/E) | Threat | Attack vector |
|---------|------------------------|--------|---------------|
|         |                        |        |               |
|         |                        |        |               |
|         |                        |        |               |
|         |                        |        |               |
|         |                        |        |               |

Plausibility rule: if you can't describe the attack vector, it goes to the
parking lot, not the model.

## 3. Risk scoring

`risk = likelihood (1–5) × impact (1–5)`

| Threat | Likelihood | Impact | Risk | Priority |
|--------|-----------|--------|------|----------|
|        |           |        |      |          |
|        |           |        |      |          |
|        |           |        |      |          |

| Risk   | Action                                        |
|--------|-----------------------------------------------|
| 15–25  | Fix before shipping; block the release        |
| 8–14   | Mitigate in the current or next sprint        |
| 3–7    | Schedule; document the acceptance             |
| 1–2    | Accept and note why                           |

## 4. Mitigation register

| # | Mitigation | Owner | Target sprint/date | Status |
|---|------------|-------|--------------------|--------|
|   |            |       |                    |        |
|   |            |       |                    |        |
|   |            |       |                    |        |

Accepted risks (document explicitly — an auditor reads these differently
than forgotten ones):

## 5. Close-out

- [ ] Every threat has a mitigation or a documented acceptance
- [ ] Every mitigation has an owner
- [ ] Revisit date agreed: ______________
- [ ] Model stored where the team actually looks (repo docs/, not a wiki orphan)
