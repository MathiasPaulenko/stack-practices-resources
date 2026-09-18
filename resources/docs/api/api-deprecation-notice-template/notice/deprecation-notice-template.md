# API Deprecation Notice: `<Endpoint / Field / Version>`

**API:** `api.example.com/v1/...`
**Deprecated Since:** `YYYY-MM-DD`
**Sunset Date:** `YYYY-MM-DD` (NN days notice)
**Severity:** `Breaking Change` | `Non-Breaking Deprecation`

## What is Changing

### Before
```
GET /v1/orders?customer_id=123
Response: { "order_id": "abc", "total": 100.00 }
```

### After
```
GET /v2/orders?customerId=123
Response: { "orderId": "abc", "totalAmount": 100.00 }
```

## Why This Change is Happening

- <reason 1 — e.g. align field naming with company-wide camelCase standard>
- <reason 2 — e.g. consolidate v1 and v2 data models>
- <reason 3>

## Migration Steps

1. **Update field names:** <old> → <new>
2. **Update response parsing:** <old field> → <new field> (same data type)
3. **Switch endpoint:** <old base path> → <new base path>
4. **Test in sandbox:** Validate against `sandbox-api.example.com/v2`
5. **Deploy to production:** Before `YYYY-MM-DD`

## Timeline

| Milestone | Date | Action Required |
|-----------|------|-----------------|
| Notice Sent | YYYY-MM-DD | Review migration guide |
| Sandbox Available | YYYY-MM-DD | Begin testing new endpoints |
| Old Version Marked Deprecated | YYYY-MM-DD | Monitor deprecation headers |
| Final Reminder | YYYY-MM-DD | Complete migration or request extension |
| Sunset | YYYY-MM-DD | Old version returns 410 Gone |

## Support & Contact

- **Migration Guide:** https://docs.example.com/api-migration
- **Sandbox Environment:** https://sandbox-api.example.com
- **Support Email:** api-support@example.com
- **Office Hours:** <day + time>

## Exceptions

If you cannot migrate before the sunset date, contact us at
api-support@example.com with:
- Your use case
- Estimated migration timeline
- Blockers preventing timely migration
