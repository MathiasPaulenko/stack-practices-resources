import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class FormatDate {
    public static void main(String[] args) {
        ZonedDateTime now = ZonedDateTime.parse("2026-06-10T14:30:00Z");
        System.out.println(now.format(DateTimeFormatter.ISO_INSTANT));
        System.out.println(now.withZoneSameInstant(ZoneId.of("Europe/Madrid"))
            .format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm z")));
    }
}
