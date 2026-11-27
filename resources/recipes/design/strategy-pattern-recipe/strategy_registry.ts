class StrategyRegistry<TContext, TResult> {
  private strategies: Map<string, (ctx: TContext) => TResult> = new Map();

  register(key: string, strategy: (ctx: TContext) => TResult): void {
    this.strategies.set(key, strategy);
  }

  select(context: TContext & { strategyKey?: string }): (ctx: TContext) => TResult {
    const key = context.strategyKey;
    if (!key || !this.strategies.has(key)) {
      throw new Error(`No strategy registered for key: ${key}`);
    }
    return this.strategies.get(key)!;
  }
}

// Registration at startup
const shippingRegistry = new StrategyRegistry<Order, number>();

shippingRegistry.register('flat-rate', (order) => 10);
shippingRegistry.register('weight-based', (order) => order.totalWeight * 2.5);
shippingRegistry.register('distance', (order) => 5 + order.distanceKm * 0.5);
shippingRegistry.register('free-shipping', (order) => {
  const subtotal = order.items.reduce((s, i) => s + i.price, 0);
  return subtotal > 100 ? 0 : 10;
});

// Usage — select strategy by key from order metadata
const calculate = shippingRegistry.select(order as Order & { strategyKey: string });
const shipping = calculate(order);
