# Hexagonal Architecture — Companion Files

Runnable ports-and-adapters example for the StackPractices recipe
[Build Maintainable Applications with Hexagonal Architecture](https://stackpractices.com/recipes/hexagonal-architecture/).

## Files

| File | Contents |
|------|----------|
| `ports.ts` | Secondary ports: `UserRepository`, `EmailService` |
| `user-registration-service.ts` | Domain entity `User` + `UserRegistrationService` (primary port implementation) |
| `adapters.ts` | Driven adapters: `PostgresUserRepository`, `InMemoryUserRepository`, `SmtpEmailService`, `MockEmailService` |
| `unit-of-work.ts` | `UnitOfWork` port, `OrderService` use case, `PostgresUnitOfWork` adapter |
| `main.ts` | Composition root: wires Postgres + SMTP adapters and exposes an Express route |
| `user-registration-service.test.ts` | Vitest unit tests running fully in memory |
| `hexagonal.py` | Python variant: ABC ports, domain service, in-memory adapter |

## Usage

```bash
# Run the domain tests (no database needed)
npm install vitest
npx vitest run user-registration-service.test.ts
```

To run `main.ts` you need a PostgreSQL database, `DATABASE_URL`, and
`express` + `pg` installed. Swap `PostgresUserRepository` for
`InMemoryUserRepository` in `main.ts` to boot without a database.
