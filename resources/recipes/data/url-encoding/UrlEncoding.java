import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class UrlEncoding {

    public static String encodeValue(String value) {
        return URLEncoder.encode(value, StandardCharsets.UTF_8);
    }

    public static String decodeValue(String encoded) {
        return URLDecoder.decode(encoded, StandardCharsets.UTF_8);
    }

    public static String buildQuery(Map<String, String> params) {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, String> entry : params.entrySet()) {
            if (sb.length() > 0) sb.append("&");
            sb.append(URLEncoder.encode(entry.getKey(), StandardCharsets.UTF_8));
            sb.append("=");
            sb.append(URLEncoder.encode(entry.getValue(), StandardCharsets.UTF_8));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Encode
        String encoded = encodeValue("hello world & friends");
        System.out.println("Encoded: " + encoded); // hello+world+%26+friends

        // Build query string
        Map<String, String> params = new LinkedHashMap<>();
        params.put("search", "python & java");
        params.put("page", "2");
        String query = buildQuery(params);
        System.out.println("Query: " + query); // search=python+%26+java&page=2

        // Parse URI
        try {
            URI parsed = new URI("https://api.example.com/search?query=hello%20world&limit=10");
            System.out.println("Query: " + parsed.getQuery()); // query=hello%20world&limit=10
        } catch (URISyntaxException e) {
            System.err.println("Invalid URI: " + e.getMessage());
        }

        // Decode
        String decoded = decodeValue("hello%20world");
        System.out.println("Decoded: " + decoded); // hello world
    }
}
