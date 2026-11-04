package domain;

import java.util.HashMap;
import java.util.Map;

public class OrderService {
    private final Map<Long, Order> orders = new HashMap<>();

    public Order create(OrderRequest request) {
        if (request.itemId() == null || request.itemId().isBlank()) {
            throw new ValidationException("Item ID is required");
        }
        if (request.quantity() <= 0) {
            throw new ValidationException("Quantity must be positive");
        }
        Order order = new Order(request.itemId(), request.quantity());
        orders.put(order.getId(), order);
        return order;
    }

    public void ship(long orderId) {
        orders.get(orderId).setStatus(OrderStatus.SHIPPED);
    }

    public void cancel(long orderId) {
        Order order = orders.get(orderId);
        if (order.getStatus() == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Shipped orders cannot be canceled");
        }
        order.setStatus(OrderStatus.CANCELED);
    }
}
