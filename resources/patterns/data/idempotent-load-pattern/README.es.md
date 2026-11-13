# Patrón Carga Idempotente — Archivos complementarios

Piezas ejecutables del patrón
[Carga Idempotente: Re-ejecutar Loads sin Duplicados](https://stackpractices.com/es/patterns/idempotent-load-pattern/):
una sentencia upsert y una demo Python autocontenida que podés correr dos veces.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `idempotent_upsert.sql` | Upsert MERGE canónico: las filas existentes se actualizan, las nuevas se insertan, las re-ejecuciones no cambian nada. |
| `idempotent_load.py` | Demo SQLite autocontenida del patrón completo: chequeo de load ID en historial, upsert, registro transaccional. Correr el mismo batch dos veces imprime `skipped`; un batch cambiado hace upsert sin duplicar. |

## Ejecutar

```bash
python idempotent_load.py   # sin dependencias — solo sqlite3 de stdlib
```
