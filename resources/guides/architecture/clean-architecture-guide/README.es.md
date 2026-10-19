# Clean Architecture — Ejemplo de Registro de Usuarios

Ejemplo ejecutable en TypeScript para la [guía de Clean Architecture](https://stackpractices.com/es/guides/clean-architecture-guide/) de StackPractices.

Un flujo de `POST /users` repartido en las cuatro capas de Clean Architecture. Todas las reglas de negocio viven en `domain/` y `application/`; los frameworks y el I/O se quedan en `infrastructure/` y `presentation/`.

## Estructura

```text
domain/          Reglas de negocio de empresa (entidades, value objects, puertos)
  entities/      User
  valueobjects/  Email, UserId, UserStatus
  repositories/  Puerto UserRepository (interfaz)
  services/      Puerto EmailService (interfaz)
application/     Reglas de negocio de aplicación (casos de uso, DTOs, Result)
  usecases/      RegisterUserUseCase
infrastructure/  Adaptadores: repo Postgres, repo en memoria, mailer espía
presentation/    UserController (DTO HTTP <-> comando de dominio)
tests/           Tests Jest — dominio puro + caso de uso con fakes
```

## Cómo funciona

1. `UserController.register(dto)` traduce el DTO de HTTP a `RegisterUserCommand`.
2. `RegisterUserUseCase` comprueba duplicados a través del puerto `UserRepository`, crea la entidad `User`, la guarda y llama al puerto `EmailService`.
3. `PostgresUserRepository` / `InMemoryUserRepository` implementan el puerto; el caso de uso nunca ve con cuál está hablando.

## Ejecutar los tests

Las suites de dominio y casos de uso no necesitan base de datos — corren contra `InMemoryUserRepository` y `SpyEmailService`:

```bash
npm install -D typescript ts-jest @types/jest jest
npx jest tests/
```

Para usar el adaptador de Postgres, pasa una instancia de Knex (`npm i knex pg`) y conéctala en la composition root (`app.ts` en un proyecto real):

```typescript
const useCase = new RegisterUserUseCase(
  new PostgresUserRepository(knex),
  new SendGridEmailService(apiKey)
);
const controller = new UserController(useCase);
```

## La Regla de Dependencia en una línea

`infrastructure/` importa las interfaces de `domain/`. `domain/` no importa nada de `infrastructure/`. Cada flecha del código fuente apunta hacia adentro.
