# Deprecation Notice: User Service API v2

**Status:** Deprecated as of 2026-09-15. Sunset date: 2026-12-31.

**What changes:** `GET /v2/users/{id}` is replaced by `GET /v3/users/{id}`.
The `name` field splits into `firstName` and `lastName`, and error
responses now use RFC 7807 Problem Details.

**What to do:** Follow the migration guide and test against
`https://sandbox.api.example.com/v3/` before 2026-12-01.

**What happens if you don't:** after 2026-12-31 the endpoint returns
`410 Gone` with a body pointing to the v3 documentation.

**Contact:** platform-team@example.com — office hours Tuesdays 15:00 UTC.
