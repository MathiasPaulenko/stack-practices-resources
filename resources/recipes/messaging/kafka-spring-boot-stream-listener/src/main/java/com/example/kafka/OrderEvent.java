package com.example.kafka;

public class OrderEvent {

    private String orderId;
    private String userId;
    private double total;

    public OrderEvent() {
    }

    public OrderEvent(String orderId, String userId, double total) {
        this.orderId = orderId;
        this.userId = userId;
        this.total = total;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public double getTotal() {
        return total;
    }

    public void setTotal(double total) {
        this.total = total;
    }

    @Override
    public String toString() {
        return "OrderEvent{orderId=" + orderId + ", userId=" + userId + ", total=" + total + "}";
    }
}
