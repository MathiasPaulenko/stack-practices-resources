// acl/LegacyCustomerTranslator.ts — the only file that knows stat_cd exists
const STATUS_MAP: Record<string, CustomerStatus> = {
  '1': CustomerStatus.active,
  '2': CustomerStatus.suspended,
  '3': CustomerStatus.closed,
};
const CURRENCY_MAP: Record<string, Currency> = {
  '1': 'USD', '2': 'EUR', '3': 'GBP',
};

export function toDomain(raw: LegacyCustomerXml): Customer {
  return {
    id: String(raw.cust_id),
    name: raw.nm.trim(),                      // "J. SMITH  " → "J. SMITH"
    status: STATUS_MAP[raw.stat_cd] ?? CustomerStatus.unknown,
    currency: CURRENCY_MAP[raw.crncy] ?? 'USD',
    lastPurchase: parseLegacyDate(raw.last_purch_dt),  // 20231114 → Date
  };
}
