# Arquitectura Hexagonal — Archivos complementarios

Ejemplo ejecutable de ports y adapters para la receta de StackPractices
[Construir Aplicaciones Mantenibles con Arquitectura Hexagonal](https://stackpractices.com/es/recipes/hexagonal-architecture/).

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `ports.ts` | Ports secundarios: `UserRepository`, `EmailService` |
| `user-registration-service.ts` | Entidad de dominio `User` + `UserRegistrationService` (implementación del port primario) |
| `adapters.ts` | Adapters de salida: `PostgresUserRepository`, `InMemoryUserRepository`, `SmtpEmailService`, `MockEmailService` |
| `unit-of-work.ts` | Port `UnitOfWork`, caso de uso `OrderService`, adapter `PostgresUnitOfWork` |
| `main.ts` | Raíz de composición: conecta los adapters Postgres + SMTP y expone una ruta Express |
| `user-registration-service.test.ts` | Tests unitarios con Vitest que corren completamente en memoria |
| `hexagonal.py` | Variante Python: ports ABC, domain service, adapter en memoria |

## Uso

```bash
# Ejecuta los tests de dominio (sin base de datos)
npm install vitest
npx vitest run user-registration-service.test.ts
```

Para ejecutar `main.ts` necesitas una base de datos PostgreSQL, la variable
`DATABASE_URL` y los paquetes `express` + `pg`. Cambia
`PostgresUserRepository` por `InMemoryUserRepository` en `main.ts` para
arrancar sin base de datos.
