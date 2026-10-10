import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.File;
import java.io.StringWriter;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

public class JsonToCsv {
    public static void main(String[] args) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> records = mapper.readValue(
            new File("data/sample.json"), List.class);

        // Union of keys across all records, sorted for stable column order
        TreeSet<String> headers = new TreeSet<>();
        for (Map<String, Object> record : records) {
            headers.addAll(record.keySet());
        }

        StringWriter sw = new StringWriter();
        try (CSVPrinter printer = new CSVPrinter(sw,
                CSVFormat.DEFAULT.builder()
                    .setHeader(headers.toArray(new String[0]))
                    .build())) {
            for (Map<String, Object> record : records) {
                for (String header : headers) {
                    printer.print(record.getOrDefault(header, ""));
                }
                printer.println();
            }
        }
        System.out.println(sw);
    }
}
