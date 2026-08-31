import de.mkammerer.argon2.Argon2;
import de.mkammerer.argon2.Argon2Factory;

public class HashArgon2 {
    public static void main(String[] args) {
        Argon2 argon2 = Argon2Factory.create(Argon2Factory.Argon2Types.ARGON2id);
        char[] password = "supersecret".toCharArray();

        long start = System.nanoTime();
        String hash = argon2.hash(3, 65536, 1, password);
        double hashMs = (System.nanoTime() - start) / 1_000_000.0;

        boolean ok = argon2.verify(hash, password);

        System.out.printf("Argon2id hash: %s%n", hash);
        System.out.printf("hash time: %.2f ms%n", hashMs);
        System.out.printf("verify: %b%n", ok);

        argon2.wipeArray(password);
    }
}
