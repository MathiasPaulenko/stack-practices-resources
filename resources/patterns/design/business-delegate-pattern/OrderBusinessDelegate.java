// Business Delegate as used in J2EE: lookup, cached reference, exception translation.
import java.util.*;

interface OrderService {
    Map<String, Object> createOrder(String customerId, List<String> items);
    Map<String, Object> getOrder(String orderId);
}

class RemoteOrderService implements OrderService {
    public Map<String, Object> createOrder(String customerId, List<String> items) {
        Map<String, Object> result = new HashMap<>();
        result.put("order_id", "ORD-123");
        result.put("status", "created");
        result.put("items", items);
        return result;
    }

    public Map<String, Object> getOrder(String orderId) {
        Map<String, Object> result = new HashMap<>();
        result.put("order_id", orderId);
        result.put("status", "shipped");
        return result;
    }
}

class ServiceLocator {
    private static final Map<String, Object> services = new HashMap<>();
    public static void register(String name, Object service) { services.put(name, service); }
    public static Object lookup(String name) { return services.get(name); }
}

public class OrderBusinessDelegate {
    private OrderService service;

    private OrderService getService() {
        if (service == null) {
            service = (OrderService) ServiceLocator.lookup("OrderService");
            if (service == null) service = new RemoteOrderService();
        }
        return service;
    }

    public Map<String, Object> createOrder(String customerId, List<String> items) {
        try {
            return getService().createOrder(customerId, items);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create order: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> getOrder(String orderId) {
        return getService().getOrder(orderId);
    }

    public static void main(String[] args) {
        ServiceLocator.register("OrderService", new RemoteOrderService());
        OrderBusinessDelegate delegate = new OrderBusinessDelegate();
        Map<String, Object> result = delegate.createOrder("CUST-001", List.of("item1", "item2"));
        System.out.println("Order created: " + result.get("order_id"));
    }
}
