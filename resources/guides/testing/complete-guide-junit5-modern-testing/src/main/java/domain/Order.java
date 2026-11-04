package domain;

import java.util.concurrent.atomic.AtomicLong;

public class Order {
    private static final AtomicLong IDS = new AtomicLong(1);

    private final long id;
    private final String itemId;
    private final int quantity;
    private OrderStatus status = OrderStatus.PENDING;

    public Order(String itemId, int quantity) {
        this.id = IDS.getAndIncrement();
        this.itemId = itemId;
        this.quantity = quantity;
    }

    public long getId() {
        return id;
    }

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
    }
}
