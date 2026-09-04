# Repository Pattern — Companion Resource

Companion code for the StackPractices pattern [Repository Pattern](https://stackpractices.com/patterns/repository-pattern/).

## Contents

- `user_repository.py` — Python implementation with abstract interface, in-memory repository, and domain service.
- `user_repository.js` — JavaScript implementation with the same structure.
- `UserRepository.java` — Java implementation with interface and in-memory repository.
- `test_repository.py` — Pytest tests covering CRUD, filtering, and service logic.
- `meta.json` — Resource metadata.

## Running the tests

```bash
pip install pytest
pytest test_repository.py -v
```

## Key concepts

- **Repository interface**: abstract contract that all implementations must satisfy.
- **In-memory repository**: fast, deterministic tests without a database.
- **Domain service**: depends on the interface, not the concrete class.
- **Aggregate root**: repositories are per aggregate, not per entity.
