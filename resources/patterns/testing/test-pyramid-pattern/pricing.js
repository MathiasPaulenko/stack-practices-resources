// Pricing domain logic used by the unit test examples.

export function parsePrice(raw) {
  const value = Number.parseFloat(raw);
  if (Number.isNaN(value) || value < 0) {
    throw new TypeError(`Invalid price: ${raw}`);
  }
  return value;
}

export function applyDiscount(total, rate) {
  const discounted = total * (1 - rate);
  return Math.max(0, discounted);
}
