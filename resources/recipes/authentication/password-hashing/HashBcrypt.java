import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class HashBcrypt {
    public static void main(String[] args) {
        String password = "supersecret";
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);

        long start = System.nanoTime();
        String hashed = encoder.encode(password);
        double hashMs = (System.nanoTime() - start) / 1_000_000.0;

        boolean ok = encoder.matches(password, hashed);

        System.out.printf("bcrypt hash: %s%n", hashed);
        System.out.printf("hash time: %.2f ms%n", hashMs);
        System.out.printf("verify: %b%n", ok);
    }
}
