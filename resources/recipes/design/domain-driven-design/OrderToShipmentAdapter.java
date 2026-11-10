// Anti-corruption layer between the Order and Shipping bounded contexts.
// Shipping never sees the Order model — it receives a ShipmentRequest
// built by this adapter. When Order changes, only this file follows.

public class OrderToShipmentAdapter {
    public ShipmentRequest adapt(OrderSubmittedEvent event, Order order) {
        return new ShipmentRequest(
            event.getOrderId().toString(),
            order.getShippingAddress(),
            order.getLines().stream()
                .map(line -> new PackageSpec(line.getProductId(), line.getQuantity()))
                .collect(Collectors.toList())
        );
    }
}
