// Specification pattern: composable, named business rules.
export interface Specification<T> {
  isSatisfiedBy(candidate: T): boolean;
  and(other: Specification<T>): Specification<T>;
  or(other: Specification<T>): Specification<T>;
  not(): Specification<T>;
}

export class AndSpecification<T> implements Specification<T> {
  constructor(private left: Specification<T>, private right: Specification<T>) {}

  isSatisfiedBy(candidate: T): boolean {
    return this.left.isSatisfiedBy(candidate) && this.right.isSatisfiedBy(candidate);
  }
  and(other: Specification<T>): Specification<T> {
    return new AndSpecification(this, other);
  }
  or(other: Specification<T>): Specification<T> {
    return new OrSpecification(this, other);
  }
  not(): Specification<T> {
    return new NotSpecification(this);
  }
}

export class OrSpecification<T> implements Specification<T> {
  constructor(private left: Specification<T>, private right: Specification<T>) {}

  isSatisfiedBy(candidate: T): boolean {
    return this.left.isSatisfiedBy(candidate) || this.right.isSatisfiedBy(candidate);
  }
  and(other: Specification<T>): Specification<T> {
    return new AndSpecification(this, other);
  }
  or(other: Specification<T>): Specification<T> {
    return new OrSpecification(this, other);
  }
  not(): Specification<T> {
    return new NotSpecification(this);
  }
}

export class NotSpecification<T> implements Specification<T> {
  constructor(private inner: Specification<T>) {}

  isSatisfiedBy(candidate: T): boolean {
    return !this.inner.isSatisfiedBy(candidate);
  }
  and(other: Specification<T>): Specification<T> {
    return new AndSpecification(this, other);
  }
  or(other: Specification<T>): Specification<T> {
    return new OrSpecification(this, other);
  }
  not(): Specification<T> {
    return new NotSpecification(this);
  }
}

// Example rule: an order can be cancelled while submitted and not yet shipped.
interface Order {
  status: string;
  hasShipped(): boolean;
  isPaid(): boolean;
}

class OrderCanBeCancelledSpec implements Specification<Order> {
  isSatisfiedBy(order: Order): boolean {
    return order.status === "submitted" && !order.hasShipped();
  }
  and(other: Specification<Order>): Specification<Order> {
    return new AndSpecification(this, other);
  }
  or(other: Specification<Order>): Specification<Order> {
    return new OrSpecification(this, other);
  }
  not(): Specification<Order> {
    return new NotSpecification(this);
  }
}

class OrderNotPaidSpec implements Specification<Order> {
  isSatisfiedBy(order: Order): boolean {
    return !order.isPaid();
  }
  and(other: Specification<Order>): Specification<Order> {
    return new AndSpecification(this, other);
  }
  or(other: Specification<Order>): Specification<Order> {
    return new OrSpecification(this, other);
  }
  not(): Specification<Order> {
    return new NotSpecification(this);
  }
}

export const canCancelOrder = new OrderCanBeCancelledSpec().and(
  new OrderNotPaidSpec()
);
