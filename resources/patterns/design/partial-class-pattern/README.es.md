# Patrón Partial Class — Companion en C\#

Archivos ejecutables de acompañamiento para el patrón de StackPractices
[Patrón Partial Class](https://stackpractices.com/es/patterns/partial-class-pattern/).

## Requisitos

- .NET 8 SDK o superior

## Inicio rápido

```bash
# Compilar y ejecutar
dotnet run

# O solo compilar
dotnet build
```

## Archivos

- `Customer.generated.cs` — propiedades generadas (`Id`, `Name`, `Email`).
- `Customer.custom.cs` — lógica de validación y presentación escrita a mano.
- `Order.cs` — modelo principal del pedido.
- `Order.Validation.cs` — reglas de validación.
- `Order.Pricing.cs` — descuentos, cupones e impuestos.
- `Order.Serialization.cs` — helpers de serialización JSON.
- `OrderItem.cs` — línea del pedido.
- `CouponService.cs` — stub simple de validación de cupones.
- `Program.cs` — demostración de uso.

El compilador fusiona cada archivo `partial class Order` en un único tipo `Order`.
Editá solo los archivos `*.custom.cs` si el modelo se regenera desde una base de
datos u otra fuente.
