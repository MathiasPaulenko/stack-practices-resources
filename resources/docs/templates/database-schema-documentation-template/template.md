# Schema Documentation: [Database Name]

## Overview
- **Engine:** PostgreSQL 16 / MySQL 8 / etc.
- **Purpose:** One paragraph describing what this database stores and which services read/write to it.
- **Owner team:** [team name]
- **Replication:** [none / streaming / logical]
- **Backup schedule:** [daily / hourly / continuous]

## Entities

### Table: users

**Purpose:** Stores authenticated user accounts for the application.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | uuid | NO | gen_random_uuid() | Primary key, generated server-side |
| email | varchar(255) | NO | — | Unique, lowercase on insert via trigger |
| password_hash | varchar(255) | NO | — | Argon2id hash, never log or expose |
| display_name | varchar(100) | YES | NULL | User-chosen name, shown in UI |
| status | smallint | NO | 1 | 0=deleted, 1=active, 2=suspended, 3=pending_verification |
| metadata | jsonb | YES | '{}' | Flexible key-value store for feature flags, preferences |
| created_at | timestamptz | NO | now() | Row creation timestamp |
| updated_at | timestamptz | NO | now() | Updated via trigger on every UPDATE |
| deleted_at | timestamptz | YES | NULL | Soft delete marker; filtered by application queries |

**Constraints:**
- `users_email_key` — UNIQUE on `email`
- `users_status_check` — CHECK (status >= 0 AND status <= 3)

**Indexes:**
| Name | Columns | Type | Purpose | Added in migration |
|------|---------|------|---------|-------------------|
| users_pkey | id | btree | Primary key | 001_initial |
| users_email_key | email | btree | Login lookup, uniqueness | 001_initial |
| users_status_idx | status | btree | Filter active users in admin panel | 014_admin_dashboard |
| users_created_at_idx | created_at | btree | Pagination by creation date | 022_pagination |

**Business rules:**
- Email is lowercased on insert and update via a trigger
- `status = 0` (deleted) is set by the application, never by a direct SQL update
- `metadata` must not contain PII — enforced by application validation, not DB constraint
- `deleted_at` is set when status changes to 0; both fields must agree

### Table: orders

**Purpose:** Stores customer orders, linked to the user who placed them.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | uuid | NO | gen_random_uuid() | Primary key |
| user_id | uuid | NO | — | FK to users.id, CASCADE DELETE |
| total_cents | integer | NO | 0 | Total in cents, never float |
| currency | char(3) | NO | 'USD' | ISO 4217 currency code |
| status | smallint | NO | 0 | 0=pending, 1=paid, 2=shipped, 3=delivered, 4=cancelled, 5=refunded |
| placed_at | timestamptz | NO | now() | When the order was placed |
| shipped_at | timestamptz | YES | NULL | When the order was shipped |

**Constraints:**
- `orders_user_id_fkey` — FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `orders_total_check` — CHECK (total_cents >= 0)
- `orders_currency_check` — CHECK (currency IN ('USD', 'EUR', 'GBP', 'JPY'))

**Indexes:**
| Name | Columns | Type | Purpose | Added in migration |
|------|---------|------|---------|-------------------|
| orders_pkey | id | btree | Primary key | 001_initial |
| orders_user_id_idx | user_id | btree | List orders by user | 001_initial |
| orders_status_placed_at_idx | status, placed_at | btree | Admin dashboard: filter by status, sort by date | 014_admin_dashboard |

**Business rules:**
- `total_cents` is stored as integer to avoid floating-point errors
- Orders with `status >= 2` can't be cancelled (application enforces)
- `shipped_at` must be null when `status < 2` (application enforces)

## Relationships

```
users 1───∞ orders
  │              │
  │              └── order_items (line items per order)
  │
  └── user_preferences (1:1, optional)
```

- **users → orders**: One user can have many orders. CASCADE DELETE removes orders when a user is hard-deleted (rare; soft delete is preferred).
- **orders → order_items**: One order has many line items. CASCADE DELETE.
- **users → user_preferences**: One-to-one, LEFT JOIN. Preferences are optional.

## Enum Reference

| Table | Column | Value | Meaning |
|-------|--------|-------|---------|
| users | status | 0 | Deleted (soft) |
| users | status | 1 | Active |
| users | status | 2 | Suspended (admin action) |
| users | status | 3 | Pending email verification |
| orders | status | 0 | Pending payment |
| orders | status | 1 | Paid, awaiting shipment |
| orders | status | 2 | Shipped |
| orders | status | 3 | Delivered |
| orders | status | 4 | Cancelled |
| orders | status | 5 | Refunded |

## Migration History

| Version | Date | Description | Author | Rollback notes |
|---------|------|-------------|--------|----------------|
| 001 | 2026-01-15 | Initial schema (users, orders, order_items) | Mathias | Drop all tables |
| 014 | 2026-03-02 | Add admin dashboard indexes | Mathias | DROP INDEX orders_status_placed_at_idx; DROP INDEX users_status_idx; |
| 022 | 2026-05-10 | Add pagination index on users.created_at | Mathias | DROP INDEX users_created_at_idx; |

## Deprecated Columns

| Table | Column | Deprecated on | Removal target | Replacement |
|-------|--------|---------------|----------------|-------------|
| users | legacy_id | 2026-04-01 | 2026-07-01 | Migrated to `id` (uuid) in migration 018 |

## Notes

- All timestamps are stored as `timestamptz` in UTC. Application converts to user timezone on display.
- Monetary values are stored as integer cents, never as float or numeric.
- Soft deletes use `deleted_at` + `status = 0`. Hard deletes require a documented reason and a migration.
- The `metadata` jsonb column is for non-structured data only. If a key becomes queried regularly, promote it to a real column.
