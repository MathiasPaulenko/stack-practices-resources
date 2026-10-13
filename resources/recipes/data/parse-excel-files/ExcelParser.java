import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.FileInputStream;

// Runnable Excel (.xlsx) example with Apache POI.
// Companion to https://stackpractices.com/recipes/parse-excel-files/
// Dependency (Maven): org.apache.poi:poi-ooxml:5.3.0
public class ExcelParser {
    public static void main(String[] args) throws Exception {
        String file = args.length > 0 ? args[0] : "sample.xlsx";
        try (Workbook wb = new XSSFWorkbook(new FileInputStream(file))) {
            Sheet sheet = wb.getSheetAt(0);
            for (Row row : sheet) {
                for (Cell cell : row) {
                    System.out.print(cell + "\t");
                }
                System.out.println();
            }
        }
    }
}
