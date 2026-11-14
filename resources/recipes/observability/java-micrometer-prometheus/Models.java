// Shared model types used by the metrics examples.
// In a real service these live in your domain package — they are records here
// so every example compiles against the same shapes.

public final class Models {

    private Models() {
    }

    public record OrderRequest(String customerId, int itemCount, double total) {
    }

    public record PaymentRequest(String orderId, double amount, String currency) {
    }

    public record PaymentResult(String status) {
    }

    public record User(long id, String email) {
    }
}
