// Java Spring Boot saga orchestrator with event-sourced state
// From https://stackpractices.com/recipes/saga-pattern-recipe/

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderSagaManager {

    private final OrderRepository orderRepo;
    private final SagaStateRepository sagaStateRepo;
    private final InventoryClient inventoryClient;
    private final PaymentClient paymentClient;
    private final ShippingClient shippingClient;

    public OrderSagaManager(OrderRepository orderRepo,
                            SagaStateRepository sagaStateRepo,
                            InventoryClient inventoryClient,
                            PaymentClient paymentClient,
                            ShippingClient shippingClient) {
        this.orderRepo = orderRepo;
        this.sagaStateRepo = sagaStateRepo;
        this.inventoryClient = inventoryClient;
        this.paymentClient = paymentClient;
        this.shippingClient = shippingClient;
    }

    @Transactional
    public SagaResult execute(OrderData orderData) {
        String sagaId = UUID.randomUUID().toString();
        SagaState state = new SagaState(sagaId, orderData.getOrderId());
        sagaStateRepo.save(state);

        try {
            // Step 1: Create order
            orderRepo.save(new Order(orderData));
            state.setCurrentStep("ORDER_CREATED");
            sagaStateRepo.save(state);

            // Step 2: Reserve inventory
            inventoryClient.reserve(orderData.getOrderId(), orderData.getItems());
            state.setCurrentStep("INVENTORY_RESERVED");
            sagaStateRepo.save(state);

            // Step 3: Process payment
            paymentClient.charge(orderData.getOrderId(), orderData.getTotal());
            state.setCurrentStep("PAYMENT_PROCESSED");
            sagaStateRepo.save(state);

            // Step 4: Schedule shipping
            shippingClient.schedule(orderData.getOrderId(), orderData.getAddress());
            state.setCurrentStep("SHIPPING_SCHEDULED");
            state.setStatus("COMPLETED");
            sagaStateRepo.save(state);

            return SagaResult.success(sagaId);

        } catch (Exception e) {
            state.setStatus("COMPENSATING");
            state.setError(e.getMessage());
            sagaStateRepo.save(state);
            compensate(state);
            state.setStatus("COMPENSATED");
            sagaStateRepo.save(state);
            return SagaResult.failure(sagaId, e.getMessage());
        }
    }

    private void compensate(SagaState state) {
        // Compensate in reverse order
        if ("SHIPPING_SCHEDULED".equals(state.getCurrentStep())) {
            shippingClient.cancel(state.getOrderId());
        }
        if ("PAYMENT_PROCESSED".equals(state.getCurrentStep()) ||
            "SHIPPING_SCHEDULED".equals(state.getCurrentStep())) {
            paymentClient.refund(state.getOrderId());
        }
        if ("INVENTORY_RESERVED".equals(state.getCurrentStep()) ||
            "PAYMENT_PROCESSED".equals(state.getCurrentStep()) ||
            "SHIPPING_SCHEDULED".equals(state.getCurrentStep())) {
            inventoryClient.release(state.getOrderId());
        }
        orderRepo.updateStatus(state.getOrderId(), "CANCELLED");
    }

    public void resume(String sagaId) {
        SagaState state = sagaStateRepo.findById(sagaId)
            .orElseThrow(() -> new SagaNotFoundException(sagaId));

        if ("COMPENSATING".equals(state.getStatus())) {
            compensate(state);
        }
    }
}
