/**
 * State Pattern — runnable Java example.
 * An order lifecycle (pending -> paid -> shipped, or -> cancelled) where each
 * state is a class that owns its behavior and its outbound transitions.
 */
interface OrderState {
    void pay(Order order);
    void ship(Order order);
    void cancel(Order order);
}

class PendingState implements OrderState {
    public void pay(Order order) {
        System.out.println("Processing payment...");
        order.transitionTo(new PaidState());
    }
    public void ship(Order order) {
        System.out.println("Cannot ship: payment pending");
    }
    public void cancel(Order order) {
        System.out.println("Order cancelled");
        order.transitionTo(new CancelledState());
    }
}

class PaidState implements OrderState {
    public void pay(Order order) {
        System.out.println("Already paid");
    }
    public void ship(Order order) {
        System.out.println("Shipping order...");
        order.transitionTo(new ShippedState());
    }
    public void cancel(Order order) {
        System.out.println("Issuing refund...");
        order.transitionTo(new CancelledState());
    }
}

class ShippedState implements OrderState {
    public void pay(Order order) {
        System.out.println("Already paid");
    }
    public void ship(Order order) {
        System.out.println("Already shipped");
    }
    public void cancel(Order order) {
        System.out.println("Cannot cancel: already shipped");
    }
}

class CancelledState implements OrderState {
    public void pay(Order order) {
        System.out.println("Cannot pay: order cancelled");
    }
    public void ship(Order order) {
        System.out.println("Cannot ship: order cancelled");
    }
    public void cancel(Order order) {
        System.out.println("Already cancelled");
    }
}

class Order {
    private OrderState state = new PendingState();

    public void transitionTo(OrderState state) {
        this.state = state;
    }

    public void pay() { state.pay(this); }
    public void ship() { state.ship(this); }
    public void cancel() { state.cancel(this); }
}

public class StatePatternDemo {
    public static void main(String[] args) {
        Order order = new Order();
        order.pay();
        order.ship();
        order.cancel(); // Cannot cancel: already shipped
    }
}
