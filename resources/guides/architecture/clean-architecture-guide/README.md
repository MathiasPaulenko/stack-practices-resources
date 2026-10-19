# Clean Architecture — User Registration Example

Runnable TypeScript example for the [Clean Architecture guide](https://stackpractices.com/guides/clean-architecture-guide/) on StackPractices.

A `POST /users` registration flow split across the four Clean Architecture layers. All business rules live in `domain/` and `application/`; frameworks and I/O stay in `infrastructure/` and `presentation/`.

## Structure

```text
domain/          Enterprise business rules (entities, value objects, ports)
  entities/      User
  valueobjects/  Email, UserId, UserStatus
  repositories/  UserRepository port (interface)
  services/      EmailService port (interface)
application/     Application business rules (use cases, DTOs, Result)
  usecases/      RegisterUserUseCase
infrastructure/  Adapters: Postgres repo, in-memory repo, spy mailer
presentation/    UserController (HTTP DTO <-> domain command)
tests/           Jest tests — pure domain + use case with fakes
```

## How it works

1. `UserController.register(dto)` translates the HTTP DTO into `RegisterUserCommand`.
2. `RegisterUserUseCase` checks for duplicates through the `UserRepository` port, creates the `User` entity, saves it, and calls the `EmailService` port.
3. `PostgresUserRepository` / `InMemoryUserRepository` implement the port; the use case never sees which one it's talking to.

## Running the tests

The domain and use-case suites need no database — they run against `InMemoryUserRepository` and `SpyEmailService`:

```bash
npm install -D typescript ts-jest @types/jest jest
npx jest tests/
```

To use the Postgres adapter, supply a Knex instance (`npm i knex pg`) and wire it at the composition root (`app.ts` in a real project):

```typescript
const useCase = new RegisterUserUseCase(
  new PostgresUserRepository(knex),
  new SendGridEmailService(apiKey)
);
const controller = new UserController(useCase);
```

## The Dependency Rule in one line

`infrastructure/` imports `domain/` interfaces. `domain/` imports nothing from `infrastructure/`. Every source-code arrow points inward.
