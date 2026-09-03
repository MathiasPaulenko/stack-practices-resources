// Anti-Corruption Layer (ACL) example in Java.
// The ACL protects the Sales bounded context from changes in the Inventory model.
// Compile: javac java_anti_corruption_layer.java
// Run: java ACLDemo

// Sales context: defines its own interface
interface InventoryService {
    boolean isAvailable(String productId, int quantity);
}

// Inventory context: has its own API model
class CheckStockRequest {
    private final String productId;
    private final int quantity;

    public CheckStockRequest(String productId, int quantity) {
        this.productId = productId;
        this.quantity = quantity;
    }

    public String getProductId() { return productId; }
    public int getQuantity() { return quantity; }
}

class CheckStockResponse {
    private final boolean available;

    public CheckStockResponse(boolean available) {
        this.available = available;
    }

    public boolean isAvailable() { return available; }
}

// Inventory API client (external system)
class InventoryApiClient {
    public CheckStockResponse checkStock(CheckStockRequest request) {
        // Simulate: always available for demo
        return new CheckStockResponse(true);
    }
}

// ACL: translates between Sales and Inventory
class InventoryServiceACL implements InventoryService {
    private final InventoryApiClient client;

    public InventoryServiceACL(InventoryApiClient client) {
        this.client = client;
    }

    @Override
    public boolean isAvailable(String productId, int quantity) {
        // Translate Sales terms to Inventory terms
        var request = new CheckStockRequest(productId, quantity);
        var response = client.checkStock(request);
        // Translate Inventory response back to Sales terms
        return response.isAvailable();
    }
}

public class java_anti_corruption_layer {
    public static void main(String[] args) {
        // Sales context uses its own interface, unaware of Inventory's API
        InventoryService inventory = new InventoryServiceACL(new InventoryApiClient());
        boolean available = inventory.isAvailable("prod-1", 5);
        System.out.println("Product available: " + available);
    }
}
