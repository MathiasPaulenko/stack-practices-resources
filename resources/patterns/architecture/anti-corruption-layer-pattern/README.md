# Anti-Corruption Layer — Legacy Translation Examples

Reference implementations for the [Anti-Corruption Layer pattern](https://stackpractices.com/patterns/anti-corruption-layer-pattern/) resource on StackPractices.

An anti-corruption layer (ACL) is a translation boundary between a new domain model and a legacy system: the domain calls the ACL in its own vocabulary, the ACL translates to the legacy format (and back), and legacy names like `stat_cd` or `CUST_ACCT` never cross into the new code.

## Contents

| File | What it is |
|------|------------|
| `customer_acl.py` | Python ACL: `Customer` domain model, `CustomerTranslator` (bidirectional `from_legacy`/`to_legacy`), `CustomerACL` facade |
| `customer_service.py` | Domain service that only knows the ACL — never the legacy client |
| `event_acl.py` | ACL for event-driven integration: legacy `CUST_ADD`/`CUST_MOD`/`CUST_DEL` → domain events |
| `database_acl.py` | ACL as a repository: domain `CustomerRepository` implemented over `LEGACY.CUSTOMERS` |
| `acl_gateway.py` | Variant: the ACL exposed as a Flask HTTP API |
| `acl_cached.py` | Variant: caching wrapper around the ACL to reduce legacy load |
| `CustomerACL.java` | Same facade in Java 17+ (Spring `@Component`, switch expressions) |
| `LegacyCustomerTranslator.ts` | TypeScript worked example: SOAP record → domain `Customer` |
| `LegacyToClientTranslator.ts` | TypeScript worked example: flat `CUST_ACCT` row → typed `Client` |
| `legacy-customer.xml` | Sample legacy SOAP payload used by `LegacyCustomerTranslator.ts` |

## Usage

These are reference implementations, not a runnable package — each file expects the legacy-side types it translates (`LegacyCustomerClient`, `CustomerRepository`, `LegacyCustomerXml`, `Money`) to come from your own codebase. Wire the facade in front of your real legacy client, keep the translator as the only file that knows legacy field names, and point the domain at the facade.

Python 3.9+ for the `.py` files (`flask` for `acl_gateway.py`), a JDK 17+ for `CustomerACL.java`, TypeScript 4.9+ for the `.ts` files.
