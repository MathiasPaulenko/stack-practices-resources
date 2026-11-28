public class TextTruncator {
    /** Pure JDK character truncation; ellipsis included in the budget. */
    public static String truncate(String text, int maxLength) {
        if (text.length() <= maxLength) return text;
        return text.substring(0, maxLength - 3).trim() + "...";
    }

    // Apache Commons Lang alternative that handles edge cases:
    // StringUtils.abbreviate(text, maxLength)

    /** Word-boundary truncation: cut at the last space inside maxLength. */
    public static String truncateWords(String text, int maxLength) {
        StringBuilder result = new StringBuilder();
        for (String word : text.split(" ")) {
            int needed = result.length() == 0 ? word.length()
                                              : result.length() + 1 + word.length();
            if (needed > maxLength) break;
            if (result.length() > 0) result.append(' ');
            result.append(word);
        }
        return result + (result.length() < text.length() ? "..." : "");
    }

    public static void main(String[] args) {
        String s = "This is a very long sentence that needs to be shortened.";
        System.out.println(truncate(s, 50));
        System.out.println(truncateWords(s, 50));
    }
}
