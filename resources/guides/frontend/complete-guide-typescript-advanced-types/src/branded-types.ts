// Branded types and smart constructors.
// The brand is compile-time only: keep the `as` inside the constructor
// so every branded value passed through validation.

declare const brand: unique symbol;
export type Brand<T, B> = T & { [brand]: B };

export type UserId = Brand<string, "UserId">;
export type OrderId = Brand<string, "OrderId">;
export type Email = Brand<string, "Email">;

// Real UUID format (8-4-4-4-12); a charset+length regex accepts 36 dashes.
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function createUserId(raw: string): UserId {
  if (!UUID_RE.test(raw)) throw new Error(`Invalid UUID: ${raw}`);
  return raw as UserId;
}

export function createOrderId(raw: string): OrderId {
  if (!UUID_RE.test(raw)) throw new Error(`Invalid UUID: ${raw}`);
  return raw as OrderId;
}

export function createEmail(raw: string): Email {
  if (!EMAIL_RE.test(raw)) throw new Error(`Invalid email: ${raw}`);
  return raw as Email;
}

export function getUser(id: UserId): UserId {
  return id;
}
