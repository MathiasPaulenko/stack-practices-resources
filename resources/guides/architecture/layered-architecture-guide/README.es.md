# Arquitectura por Capas — Layout Companion de Solución C#

Un layout de proyecto estilo .NET ejecutable que reproduce el ejemplo e-commerce de cuatro capas de la [guía de Arquitectura por Capas](https://stackpractices.com/es/guides/layered-architecture-guide/) en StackPractices.

## Estructura

```
Presentation/   -> Controladores (delgados) + wiring DI en Program.cs
Application/    -> Orquestación en OrderService, DTOs, BusinessException
Domain/         -> Entidades Order/Product con reglas reales, interfaces de repositorio
Infrastructure/ -> AppDbContext de EF Core + implementaciones de repositorio
Tests/          -> Tests unitarios xUnit + Moq (mockean la capa inferior)
```

## Reglas de dependencia que impone el layout

```
Web -> Application -> Domain
Infrastructure -> Domain   (cumple las interfaces del dominio)
Domain no depende de nada  (cero referencias externas)
```

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `Domain/Entities/Order.cs` | Entidad con reglas reales: `Create` valida cantidad/precio, `Cancel` rechaza pedidos enviados |
| `Domain/Entities/Product.cs` | El invariante de stock vive en la entidad (`DecreaseStock`) |
| `Domain/Interfaces/*.cs` | `IOrderRepository`, `IProductRepository` — propiedad del dominio |
| `Application/Services/OrderService.cs` | Orquestación: comprobar stock → crear pedido → persistir → DTO |
| `Application/Dtos/OrderDto.cs` | Un DTO en la frontera de la API; las entidades nunca se serializan |
| `Application/Exceptions/BusinessException.cs` | Las violaciones de reglas mapean a 422 en el borde del controlador |
| `Infrastructure/Persistence/*` | `AppDbContext` + repositorios EF Core que cumplen las interfaces del dominio |
| `Presentation/Controllers/OrderController.cs` | Controlador delgado: solo traduce HTTP |
| `Presentation/Program.cs` | Wiring DI — donde se conectan las capas |
| `Tests/OrderServiceTests.cs` | Los tests de aplicación mockean repositorios; sin base de datos |

## Notas

- Los tests de aplicación nunca tocan una base de datos — falsifican `IOrderRepository`/`IProductRepository`. Los tests de repositorio pertenecen a tests de integración contra una base real (p. ej. Testcontainers).
- `Order.Create` es una factory que impone invariantes, así que ningún llamador puede producir un pedido inválido — el arreglo para un modelo de dominio anémico.
- Copia cada carpeta a un .csproj del mismo nombre (`ECommerce.Web`, `ECommerce.Application`, `ECommerce.Domain`, `ECommerce.Infrastructure`) para convertir las violaciones de dependencia en errores de compilación.
