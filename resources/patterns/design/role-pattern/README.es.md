# Patrón Role — Recursos companion

Implementaciones ejecutables del Patrón Role en Python, Java y JavaScript.
Cada una modela una entidad `Person` que gana capacidades adjuntando objetos
de rol en runtime — sin explosión de la jerarquía de clases.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `role_pattern.py` | Python | Protocolo `Role` + dataclasses `CustomerRole`/`EmployeeRole`/`VendorRole`, `Person` con assign/revoke/history |
| `RolePattern.java` | Java | Interfaz `Role` + clases de rol anidadas, `Person` con chequeo de capacidad vía `canPerform` |
| `role_pattern.js` | JavaScript | El mismo modelo con registro de roles basado en `Map` e historial con timestamps ISO |

## Ejecutar los ejemplos

```bash
python role_pattern.py
javac RolePattern.java && java RolePattern
node role_pattern.js
```

Cada script asigna los roles `customer` + `employee` a Alice, verifica algunos
permisos (`browse`, `refund`, `list_products`), procesa un reembolso a través
del rol de empleado y luego revoca `customer` — todo sin tocar la identidad
de la entidad.

## Conceptos clave

- **Entidad vs rol**: `Person` solo guarda identidad; el comportamiento vive en los role objects.
- **Adjuntar/desprender en runtime**: `assignRole`/`revokeRole` mutan capacidades, no el tipo.
- **Unión de capacidades**: `canPerform` devuelve true si algún rol adjunto permite la acción.
- **Auditabilidad**: cada assign/revoke queda en un log de historial.

## Fuente

Companion del artículo de StackPractices:
<https://stackpractices.com/es/patterns/role-pattern/>
