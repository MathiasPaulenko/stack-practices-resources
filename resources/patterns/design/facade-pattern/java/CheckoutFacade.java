import java.util.List;

record CartItem(String id, double price, int qty) {}
record Address(String email, String country) {}
record OrderResult(String orderId, double total, String trackingNumber) {}

class InventoryService {
    boolean checkStock(String itemId) { return true; }
    void reserve(String itemId, int qty) {
        System.out.println("  reserved " + qty + "x " + itemId);
    }
}

class PricingService {
    double calculateTotal(List<CartItem> items) {
        return items.stream().mapToDouble(i -> i.price() * i.qty()).sum();
    }
    double applyCoupon(double total, String coupon) {
        return coupon != null && !coupon.isEmpty() ? total * 0.9 : total;
    }
}

class PaymentService {
    String charge(double amount, String token) {
        System.out.printf("  charged %.2f with %s%n", amount, token);
        return "tx_123";
    }
}

class ShippingService {
    String createLabel(Address address) { return "TRK_456"; }
    double calculateCost(Address address) { return 9.99; }
}

class NotificationService {
    void sendConfirmation(String email, String orderId) {
        System.out.println("  confirmation sent to " + email + " for " + orderId);
    }
}

public class CheckoutFacade {
    // Facade: one entry point for the whole checkout flow.
    // Services are injected, so each one stays mockable in tests.
    private final InventoryService inventory;
    private final PricingService pricing;
    private final PaymentService payment;
    private final ShippingService shipping;
    private final NotificationService notification;

    public CheckoutFacade(InventoryService inventory, PricingService pricing,
                          PaymentService payment, ShippingService shipping,
                          NotificationService notification) {
        this.inventory = inventory;
        this.pricing = pricing;
        this.payment = payment;
        this.shipping = shipping;
        this.notification = notification;
    }

    public OrderResult checkout(List<CartItem> cart, String coupon,
                                String paymentToken, Address address) {
        // 1. Check stock and reserve
        for (CartItem item : cart) {
            if (!inventory.checkStock(item.id()))
                throw new IllegalStateException("Item " + item.id() + " out of stock");
            inventory.reserve(item.id(), item.qty());
        }

        // 2. Calculate price
        double total = pricing.calculateTotal(cart);
        total = pricing.applyCoupon(total, coupon);
        total += shipping.calculateCost(address);

        // 3. Charge
        String txId = payment.charge(total, paymentToken);

        // 4. Create shipment
        String tracking = shipping.createLabel(address);

        // 5. Notify
        notification.sendConfirmation(address.email(), txId);

        return new OrderResult(txId, total, tracking);
    }

    public static void main(String[] args) {
        CheckoutFacade facade = new CheckoutFacade(
            new InventoryService(), new PricingService(), new PaymentService(),
            new ShippingService(), new NotificationService());
        List<CartItem> cart = List.of(
            new CartItem("sku-1", 25.0, 2), new CartItem("sku-2", 10.0, 1));
        Address address = new Address("ana@example.com", "ES");
        System.out.println(facade.checkout(cart, "SAVE10", "tok_abc", address));
    }
}
