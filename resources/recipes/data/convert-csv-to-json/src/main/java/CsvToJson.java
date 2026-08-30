import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

import java.io.File;
import java.util.List;

public class CsvToJson {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        File csvFile = new File("data/sample.csv");

        CsvSchema schema = CsvSchema.builder().setUseHeader(true).build();
        CsvMapper csvMapper = new CsvMapper();
        ObjectMapper jsonMapper = new ObjectMapper()
            .enable(SerializationFeature.INDENT_OUTPUT);

        List<?> rows = csvMapper
            .readerFor(java.util.Map.class)
            .with(schema)
            .readValues(csvFile)
            .readAll();

        jsonMapper.writeValue(System.out, rows);
    }
}
