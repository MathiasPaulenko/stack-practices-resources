// Phone number parsing, validation and formatting with Google's libphonenumber.
// Dependency: com.googlecode.libphonenumber:libphonenumber:8.x
// Compile & run with the jar on the classpath.

import com.google.i18n.phonenumbers.AsYouTypeFormatter;
import com.google.i18n.phonenumbers.NumberParseException;
import com.google.i18n.phonenumbers.PhoneNumberUtil;
import com.google.i18n.phonenumbers.PhoneNumberUtil.PhoneNumberFormat;
import com.google.i18n.phonenumbers.Phonenumber.PhoneNumber;

public class PhoneFormatter {
    private static final PhoneNumberUtil util = PhoneNumberUtil.getInstance();

    public static void parseAndFormat(String raw, String region) {
        System.out.println("'" + raw + "' [" + region + "] ->");
        try {
            PhoneNumber number = util.parse(raw, region);
            System.out.println("    possible: " + util.isPossibleNumber(number));
            System.out.println("    valid: " + util.isValidNumber(number));
            System.out.println("    e164: " + util.format(number, PhoneNumberFormat.E164));
            System.out.println("    international: " + util.format(number, PhoneNumberFormat.INTERNATIONAL));
            System.out.println("    national: " + util.format(number, PhoneNumberFormat.NATIONAL));
            System.out.println("    rfc3966: " + util.format(number, PhoneNumberFormat.RFC3966));
            if (number.hasExtension()) {
                System.out.println("    extension: " + number.getExtension());
            }
            System.out.println("    type: " + util.getNumberType(number));
        } catch (NumberParseException e) {
            System.out.println("    error: " + e.getMessage());
        }
        System.out.println();
    }

    public static void main(String[] args) {
        parseAndFormat("(415) 555-2671", "US");
        parseAndFormat("020 7946 0958", "GB");
        parseAndFormat("+52 55 1234 5678", "MX");
        parseAndFormat("+1 555-1234 ext. 42", "US");
        parseAndFormat("not a number", "US");

        AsYouTypeFormatter formatter = util.getAsYouTypeFormatter("US");
        String formatted = "";
        for (char ch : "4155552671".toCharArray()) {
            formatted = formatter.inputDigit(ch);
        }
        System.out.println("As-you-type: 4155552671 -> " + formatted);
    }
}
