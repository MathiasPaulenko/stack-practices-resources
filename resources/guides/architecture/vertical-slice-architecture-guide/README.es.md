# Arquitectura por Slices Verticales — Companion

Proyecto companion para la [guía de Slices Verticales](https://stackpractices.com/es/guides/vertical-slice-architecture-guide/).

## Visión General

Una API mínima en .NET 8 que demuestra Arquitectura por Slices Verticales con MediatR, Carter y FluentValidation.

## Estructura

```text
Features/
└── Orders/
    └── CreateOrder/
        ├── CreateOrderCommand.cs    # DTO de entrada
        ├── CreateOrderHandler.cs    # Lógica de negocio
        ├── CreateOrderValidator.cs  # Reglas de validación
        └── CreateOrderEndpoint.cs   # Endpoint HTTP
Common/
├── Behaviors/
│   ├── LoggingBehavior.cs           # Pipeline MediatR (logging)
│   └── ValidationBehavior.cs        # Pipeline MediatR (validación)
├── Domain/
│   ├── Order.cs                     # Entidad de dominio
│   └── Product.cs                   # Entidad de dominio
└── Infrastructure/
    └── AppDbContext.cs              # DbContext de EF Core
Program.cs                           # Configuración de DI y startup
```

## Requisitos

- .NET 8 SDK
- Paquetes NuGet: MediatR, Carter, FluentValidation, EF Core InMemory

## Ejecutar

```bash
dotnet new web -n VerticalSliceDemo
# Agregar paquetes:
# dotnet add package MediatR
# dotnet add package Carter
# dotnet add package FluentValidation.DependencyInjectionExtensions
# dotnet add package Microsoft.EntityFrameworkCore.InMemory
# Copiar los archivos de este companion al proyecto
dotnet run
```

## Probar

```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 5, "customerEmail": "test@example.com"}'
```

Esperado: `201 Created` con el DTO de la orden.
