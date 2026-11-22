import org.springframework.web.client.RestTemplate;

/**
 * Synchronous REST call with Spring's RestTemplate.
 * Companion to https://stackpractices.com/recipes/microservices-communication/
 */
public class OrderRestClient {

    private final RestTemplate rest = new RestTemplate();

    public Order getOrder(String orderId) {
        return rest.getForObject(
            "http://orders-service/orders/{id}", Order.class, orderId);
    }
}

record Order(String id, String status) {}
