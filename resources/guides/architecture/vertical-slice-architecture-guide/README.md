# Vertical Slice Architecture — Companion

Companion project for the [Vertical Slice Architecture guide](https://stackpractices.com/guides/vertical-slice-architecture-guide/).

## Overview

A minimal .NET 8 API demonstrating Vertical Slice Architecture with MediatR, Carter, and FluentValidation.

## Structure

```text
Features/
└── Orders/
    └── CreateOrder/
        ├── CreateOrderCommand.cs    # Input DTO
        ├── CreateOrderHandler.cs    # Business logic
        ├── CreateOrderValidator.cs  # Validation rules
        └── CreateOrderEndpoint.cs   # HTTP endpoint
Common/
├── Behaviors/
│   ├── LoggingBehavior.cs           # MediatR pipeline (logging)
│   └── ValidationBehavior.cs        # MediatR pipeline (validation)
├── Domain/
│   ├── Order.cs                     # Domain entity
│   └── Product.cs                   # Domain entity
└── Infrastructure/
    └── AppDbContext.cs              # EF Core DbContext
Program.cs                           # DI configuration and startup
```

## Requirements

- .NET 8 SDK
- NuGet packages: MediatR, Carter, FluentValidation, EF Core InMemory

## Run

```bash
dotnet new web -n VerticalSliceDemo
# Add packages:
# dotnet add package MediatR
# dotnet add package Carter
# dotnet add package FluentValidation.DependencyInjectionExtensions
# dotnet add package Microsoft.EntityFrameworkCore.InMemory
# Copy the files from this companion into the project
dotnet run
```

## Test

```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 5, "customerEmail": "test@example.com"}'
```

Expected: `201 Created` with the order DTO.
