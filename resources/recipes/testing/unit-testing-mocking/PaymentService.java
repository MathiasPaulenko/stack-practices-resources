// PaymentService.java — Payment processor with email dependency
public class PaymentService {
    private final EmailService emailService;

    public PaymentService(EmailService emailService) {
        this.emailService = emailService;
    }

    public PaymentResult processPayment(int amount, String userId) {
        String paymentId = "pay_" + System.currentTimeMillis();
        boolean emailSent = false;

        try {
            emailService.send(new Email(
                "user@example.com",
                "Payment received",
                "Payment of $" + amount + " processed for " + userId + "."
            ));
            emailSent = true;
        } catch (Exception e) {
            // Email failure should not block payment
            System.err.println("Email send failed: " + e.getMessage());
        }

        return new PaymentResult(paymentId, emailSent, amount, userId);
    }
}
