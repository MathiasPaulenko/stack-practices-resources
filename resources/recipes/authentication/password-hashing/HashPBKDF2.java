import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.SecureRandom;
import java.security.spec.KeySpec;

public class HashPBKDF2 {
    public static void main(String[] args) throws Exception {
        String password = "supersecret";
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);

        int iterations = 600_000;
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, 256);

        long start = System.nanoTime();
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        byte[] hash = factory.generateSecret(spec).getEncoded();
        double hashMs = (System.nanoTime() - start) / 1_000_000.0;

        String stored = "pbkdf2_sha256$" + iterations + "$" + base16(salt) + "$" + base16(hash);

        System.out.printf("PBKDF2 stored: %s%n", stored);
        System.out.printf("hash time: %.2f ms%n", hashMs);
    }

    private static String base16(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
