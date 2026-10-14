import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Base64;
import java.util.Map;

/**
 * HMAC-SHA256 request signing.
 *
 * signHeaders returns BOTH the signature and the timestamp — the server
 * needs the timestamp to reconstruct the signed message, so it must
 * travel with the request.
 */
public class RequestSigner {
    private static final String HMAC_ALGO = "HmacSHA256";

    public static Map<String, String> signHeaders(
            String secret, String method, String path, String body) throws Exception {
        String timestamp = Instant.now().toString();
        String message = String.join("\n", method, path, timestamp, body);

        Mac mac = Mac.getInstance(HMAC_ALGO);
        mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), HMAC_ALGO));
        byte[] signature = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));

        return Map.of(
            "X-Request-Timestamp", timestamp,
            "X-Request-Signature", Base64.getEncoder().encodeToString(signature)
        );
    }

    public static boolean verify(String secret, String timestamp, String signature,
                                 String method, String path, String body) throws Exception {
        String message = String.join("\n", method, path, timestamp, body);
        Mac mac = Mac.getInstance(HMAC_ALGO);
        mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), HMAC_ALGO));
        byte[] expected = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
        // Constant-time compare
        return java.security.MessageDigest.isEqual(
            Base64.getEncoder().encodeToString(expected).getBytes(StandardCharsets.UTF_8),
            signature.getBytes(StandardCharsets.UTF_8)
        );
    }

    public static void main(String[] args) throws Exception {
        Map<String, String> headers =
            signHeaders("my-secret-key", "POST", "/api/orders", "{\"item\": \"book\"}");
        boolean ok = verify("my-secret-key",
            headers.get("X-Request-Timestamp"),
            headers.get("X-Request-Signature"),
            "POST", "/api/orders", "{\"item\": \"book\"}");
        System.out.println("signature verifies: " + ok);
    }
}
