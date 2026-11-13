import java.security.MessageDigest;
import java.security.SecureRandom;

import org.bouncycastle.crypto.generators.Argon2BytesGenerator;
import org.bouncycastle.crypto.params.Argon2Parameters;
import org.bouncycastle.util.encoders.Base64;

/**
 * Argon2id password hashing with Bouncy Castle.
 * Companion to https://stackpractices.com/recipes/hash-passwords-argon2/
 * Run: mvn compile exec:java -Dexec.mainClass=HashArgon2
 */
public class HashArgon2 {
    private static final int SALT_LENGTH = 16;
    private static final int HASH_LENGTH = 32;
    private static final int ITERATIONS = 3;
    private static final int MEMORY = 65536; // KiB → 64 MiB
    private static final int PARALLELISM = 4;

    private final SecureRandom random = new SecureRandom();

    public String hash(String password) {
        byte[] salt = new byte[SALT_LENGTH];
        random.nextBytes(salt);

        Argon2Parameters params = new Argon2Parameters.Builder()
                .withSalt(salt)
                .withParallelism(PARALLELISM)
                .withMemoryAsKB(MEMORY)
                .withIterations(ITERATIONS)
                .withVersion(Argon2Parameters.ARGON2_VERSION_13)
                .build();

        Argon2BytesGenerator generator = new Argon2BytesGenerator();
        generator.init(params);

        byte[] result = new byte[HASH_LENGTH];
        generator.generateBytes(password.toCharArray(), result);

        return String.format("$argon2id$v=19$m=%d,t=%d,p=%d$%s$%s",
                MEMORY, ITERATIONS, PARALLELISM,
                Base64.toBase64String(salt), Base64.toBase64String(result));
    }

    public boolean verify(String password, String encodedHash) {
        try {
            // "$argon2id$v=19$m=..,t=..,p=..$<salt>$<hash>" splits into 6 parts
            String[] parts = encodedHash.split("\\$");
            if (parts.length != 6 || !parts[1].equals("argon2id") || !parts[2].equals("v=19")) {
                return false;
            }

            String[] params = parts[3].split(",");
            int memory = Integer.parseInt(params[0].split("=")[1]);
            int iterations = Integer.parseInt(params[1].split("=")[1]);
            int parallelism = Integer.parseInt(params[2].split("=")[1]);
            byte[] salt = Base64.decode(parts[4]);
            byte[] actual = Base64.decode(parts[5]);

            Argon2Parameters parsed = new Argon2Parameters.Builder()
                    .withSalt(salt)
                    .withParallelism(parallelism)
                    .withMemoryAsKB(memory)
                    .withIterations(iterations)
                    .withVersion(Argon2Parameters.ARGON2_VERSION_13)
                    .build();

            Argon2BytesGenerator generator = new Argon2BytesGenerator();
            generator.init(parsed);

            byte[] expected = new byte[actual.length];
            generator.generateBytes(password.toCharArray(), expected);

            // Arrays.equals exits early on the first differing byte — a timing leak
            return MessageDigest.isEqual(expected, actual);
        } catch (RuntimeException e) {
            return false; // malformed or truncated hash
        }
    }

    public static void main(String[] args) {
        HashArgon2 hasher = new HashArgon2();
        String password = "correct horse battery staple";

        long start = System.nanoTime();
        String hashed = hasher.hash(password);
        long elapsedMs = (System.nanoTime() - start) / 1_000_000;

        System.out.println("Hash:    " + hashed);
        System.out.println("Time:    " + elapsedMs + " ms (target: 250–500 ms on your hardware)");
        System.out.println("Valid:   " + hasher.verify(password, hashed));
        System.out.println("Invalid: " + hasher.verify("wrong", hashed));
        System.out.println("Garbage: " + hasher.verify(password, "not-a-hash"));
    }
}
