import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Service;

// Timer — measure operation duration. publishPercentiles computes
// approximated percentiles in-app (per instance, non-aggregable);
// use publishPercentileHistogram() when you aggregate across replicas.
@Service
public class PaymentService {

    private final Timer paymentProcessingTimer;

    public PaymentService(MeterRegistry registry) {
        this.paymentProcessingTimer = Timer.builder("payment.processing.duration")
            .description("Time spent processing payments")
            .tag("provider", "stripe")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }

    public Models.PaymentResult processPayment(Models.PaymentRequest request) {
        return paymentProcessingTimer.record(() -> {
            // ... process payment ...
            return new Models.PaymentResult("success");
        });
    }
}
