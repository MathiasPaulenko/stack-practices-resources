/**
 * Context-aware HTML escaping helpers (Java).
 *
 * Companion to https://stackpractices.com/recipes/escape-html-entities/
 *
 * Dependencies (Maven):
 *   org.apache.commons:commons-text        — broad HTML4 entity coverage
 *   org.owasp.encoder:encoder              — one function per output context
 *
 * Prefer the OWASP Encoder when a value can land in different contexts:
 * forHtml, forHtmlAttribute, forJavaScript, forUri, forCssString.
 */

import org.apache.commons.text.StringEscapeUtils;
import org.owasp.encoder.Encode;

public class HtmlEscaper {

    /** Escape text for an HTML body context (Apache Commons Text). */
    public static String escape(String input) {
        return StringEscapeUtils.escapeHtml4(input);
    }

    /** Escape text for an HTML body context (OWASP Encoder). */
    public static String forBody(String input) {
        return Encode.forHtml(input);
    }

    /** Escape text for an HTML attribute context. */
    public static String forAttribute(String input) {
        return Encode.forHtmlAttribute(input);
    }

    /** Escape text for embedding inside a <script> block. */
    public static String forJavaScript(String input) {
        return Encode.forJavaScript(input);
    }

    /** Escape text for a CSS string context. */
    public static String forCssString(String input) {
        return Encode.forCssString(input);
    }

    /** Escape text for a CSS url() context. */
    public static String forCssUrl(String input) {
        return Encode.forCssUrl(input);
    }

    /**
     * Validate a URL for use in href/src attributes.
     * The attack is the scheme, not the characters:
     * "javascript:alert(1)" has nothing HTML-escapable yet runs on click.
     */
    public static String safeUrl(String url) {
        String lower = url.toLowerCase().trim();
        boolean allowed = lower.startsWith("http://")
            || lower.startsWith("https://")
            || lower.startsWith("mailto:")
            || lower.startsWith("tel:")
            || lower.startsWith("/");
        return allowed ? Encode.forHtmlAttribute(url) : "";
    }

    public static void main(String[] args) {
        String payload = "<script>alert(\"xss\")</script>";
        System.out.println(escape(payload));
        // -> &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;

        System.out.println(safeUrl("javascript:alert(1)"));           // -> ""
        System.out.println(safeUrl("https://example.com/?a=1&b=2"));  // -> &amp;-encoded
    }
}
