# Anti-Corruption Layer — Ejemplos de Traducción Legacy

Implementaciones de referencia para el recurso [Patrón Anti-Corruption Layer](https://stackpractices.com/es/patterns/anti-corruption-layer-pattern/) de StackPractices.

Una capa anti-corrupción (ACL) es una frontera de traducción entre un modelo de dominio nuevo y un sistema legacy: el dominio llama a la ACL en su propio vocabulario, la ACL traduce al formato legacy (y de vuelta), y nombres legacy como `stat_cd` o `CUST_ACCT` nunca cruzan al código nuevo.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `customer_acl.py` | ACL en Python: modelo de dominio `Customer`, `CustomerTranslator` (bidireccional `from_legacy`/`to_legacy`), facade `CustomerACL` |
| `customer_service.py` | Servicio de dominio que solo conoce la ACL — nunca el cliente legacy |
| `event_acl.py` | ACL para integración por eventos: `CUST_ADD`/`CUST_MOD`/`CUST_DEL` legacy → eventos de dominio |
| `database_acl.py` | ACL como repositorio: `CustomerRepository` de dominio implementado sobre `LEGACY.CUSTOMERS` |
| `acl_gateway.py` | Variante: la ACL expuesta como API HTTP con Flask |
| `acl_cached.py` | Variante: wrapper con caché sobre la ACL para reducir la carga del legacy |
| `CustomerACL.java` | La misma facade en Java 17+ (Spring `@Component`, expresiones switch) |
| `LegacyCustomerTranslator.ts` | Ejemplo trabajado en TypeScript: registro SOAP → `Customer` de dominio |
| `LegacyToClientTranslator.ts` | Ejemplo trabajado en TypeScript: fila plana `CUST_ACCT` → `Client` tipado |
| `legacy-customer.xml` | Payload SOAP legacy de ejemplo que usa `LegacyCustomerTranslator.ts` |

## Uso

Son implementaciones de referencia, no un paquete ejecutable — cada archivo espera que los tipos del lado legacy que traduce (`LegacyCustomerClient`, `CustomerRepository`, `LegacyCustomerXml`, `Money`) vengan de tu propio código. Conecta la facade delante de tu cliente legacy real, mantén el traductor como el único archivo que conoce los nombres de campos legacy, y apunta el dominio a la facade.

Python 3.9+ para los `.py` (`flask` para `acl_gateway.py`), un JDK 17+ para `CustomerACL.java`, TypeScript 4.9+ para los `.ts`.
