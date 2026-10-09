import java.text.Normalizer;
import java.util.Locale;

/**
 * Generates URL-friendly slugs from arbitrary strings using
 * Normalizer NFKD + regex (JDK only, no external dependencies).
 */
public class SlugGenerator {
    public static String generateSlug(String input) {
        String normalized = Normalizer.normalize(input, Normalizer.Form.NFKD)
            .replaceAll("\\p{InCombiningDiacriticalMarks}+", "");
        return normalized.toLowerCase(Locale.ROOT)
            .replaceAll("[^\\w\\s-]", "")
            .replaceAll("[-\\s]+", "-")
            .replaceAll("^-+|-+$", "");   // Trim edge hyphens
    }

    public static void main(String[] args) {
        System.out.println(generateSlug("Hello, World! 2024"));    // hello-world-2024
        System.out.println(generateSlug("Café & Crème Brûlée"));   // cafe-creme-brulee
    }
}
