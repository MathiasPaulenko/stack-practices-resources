import java.nio.file.*;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

public class FileCopier {

    public static void copyWithAttributes(Path src, Path dest, boolean overwrite) throws Exception {
        List<CopyOption> options = new ArrayList<>();
        options.add(StandardCopyOption.COPY_ATTRIBUTES);
        if (overwrite) options.add(StandardCopyOption.REPLACE_EXISTING);
        Files.copy(src, dest, options.toArray(new CopyOption[0]));
    }

    public static void moveWithFallback(Path src, Path dest, boolean overwrite) throws Exception {
        List<CopyOption> options = new ArrayList<>();
        if (overwrite) options.add(StandardCopyOption.REPLACE_EXISTING);

        try {
            options.add(StandardCopyOption.ATOMIC_MOVE);
            Files.move(src, dest, options.toArray(new CopyOption[0]));
        } catch (AtomicMoveNotSupportedException e) {
            options.remove(StandardCopyOption.ATOMIC_MOVE);
            copyWithAttributes(src, dest, overwrite);
            Files.deleteIfExists(src);
        }
    }

    public static String sha256(Path file) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(Files.readAllBytes(file));
        StringBuilder sb = new StringBuilder();
        for (byte b : hash) sb.append(String.format("%02x", b));
        return sb.toString();
    }
}
