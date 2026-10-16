// Spring Boot upload validator: size + content-type allow-list.
// For magic-byte verification plug in Apache Tika.
// See https://stackpractices.com/recipes/file-upload-validation/
import org.springframework.web.multipart.MultipartFile;
import java.util.Set;

public class UploadValidator {
    private static final Set<String> ALLOWED =
        Set.of("image/png", "image/jpeg", "application/pdf");
    private static final long MAX_SIZE = 5L * 1024 * 1024;

    public static void validate(MultipartFile file) {
        if (file.getSize() > MAX_SIZE) {
            throw new IllegalArgumentException("File exceeds 5 MB");
        }
        String contentType = file.getContentType();
        if (!ALLOWED.contains(contentType)) {
            throw new IllegalArgumentException("MIME type not allowed: " + contentType);
        }
        // Additional: verify magic bytes with Apache Tika for untrusted inputs
    }
}
