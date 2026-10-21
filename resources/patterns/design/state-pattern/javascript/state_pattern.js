// State Pattern — runnable JavaScript example.
// An order lifecycle (pending -> paid -> shipped, or -> cancelled) where each
// state is a class that owns its behavior and its outbound transitions.

class Order {
  constructor() { this.state = new PendingState(this); }
  transitionTo(state) { this.state = state; }
  pay() { this.state.pay(); }
  ship() { this.state.ship(); }
  cancel() { this.state.cancel(); }
}

class PendingState {
  constructor(order) { this.order = order; }
  pay() {
    console.log("Processing payment...");
    this.order.transitionTo(new PaidState(this.order));
  }
  ship() { console.log("Cannot ship: payment pending"); }
  cancel() {
    console.log("Order cancelled");
    this.order.transitionTo(new CancelledState(this.order));
  }
}

class PaidState {
  constructor(order) { this.order = order; }
  pay() { console.log("Already paid"); }
  ship() {
    console.log("Shipping order...");
    this.order.transitionTo(new ShippedState(this.order));
  }
  cancel() {
    console.log("Issuing refund...");
    this.order.transitionTo(new CancelledState(this.order));
  }
}

class ShippedState {
  constructor(order) { this.order = order; }
  pay() { console.log("Already paid"); }
  ship() { console.log("Already shipped"); }
  cancel() { console.log("Cannot cancel: already shipped"); }
}

class CancelledState {
  constructor(order) { this.order = order; }
  pay() { console.log("Cannot pay: order cancelled"); }
  ship() { console.log("Cannot ship: order cancelled"); }
  cancel() { console.log("Already cancelled"); }
}

const order = new Order();
order.pay();
order.ship();
order.cancel(); // Cannot cancel: already shipped
