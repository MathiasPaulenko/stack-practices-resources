// Strategy pattern: shipping cost varies by method, chosen at runtime.
// The checkout code calls calculate() without knowing which algorithm runs.

export interface ShippingStrategy {
  readonly method: string;
  calculate(weightKg: number): number;
}

export const standardShipping: ShippingStrategy = {
  method: "standard",
  calculate: (weightKg) => weightKg * 0.5,
};

export const expressShipping: ShippingStrategy = {
  method: "express",
  calculate: (weightKg) => weightKg * 1.5,
};

export const sameDayShipping: ShippingStrategy = {
  method: "same-day",
  calculate: (weightKg) => weightKg * 3.0,
};

const strategies: Record<string, ShippingStrategy> = {
  standard: standardShipping,
  express: expressShipping,
  "same-day": sameDayShipping,
};

export function shippingCost(method: string, weightKg: number): number {
  const strategy = strategies[method];
  if (!strategy) throw new Error(`Unknown shipping method: ${method}`);
  return strategy.calculate(weightKg);
}
