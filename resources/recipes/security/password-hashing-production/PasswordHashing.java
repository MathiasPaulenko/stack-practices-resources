// Spring-style Argon2id encoder parameters (needs Spring Security on classpath:
// org.springframework.security.crypto.argon2.Argon2PasswordEncoder)
public class PasswordHashing {

    public static final int SALT_LENGTH = 16;   // bytes
    public static final int HASH_LENGTH = 32;   // bytes
    public static final int PARALLELISM = 4;    // threads
    public static final int MEMORY_KIB  = 65536; // 64 MB
    public static final int ITERATIONS  = 3;

    // With Spring Security:
    //   PasswordEncoder encoder = new Argon2PasswordEncoder(
    //       SALT_LENGTH, HASH_LENGTH, PARALLELISM, MEMORY_KIB, ITERATIONS);
    //   String hash = encoder.encode(rawPassword);
    //   boolean ok  = encoder.matches(rawPassword, storedHash);
    //   boolean upgrade = encoder.upgradeEncoding(storedHash);
}
