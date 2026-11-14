public class PaymentGatewayStatus {

    private final boolean available;
    private final long latencyMs;
    private final String version;
    private final int statusCode;

    public PaymentGatewayStatus(boolean available, long latencyMs, String version, int statusCode) {
        this.available = available;
        this.latencyMs = latencyMs;
        this.version = version;
        this.statusCode = statusCode;
    }

    public boolean isAvailable() {
        return available;
    }

    public long getLatencyMs() {
        return latencyMs;
    }

    public String getVersion() {
        return version;
    }

    public int getStatusCode() {
        return statusCode;
    }
}
