import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class ExportExcel {

    public void exportCsv(Iterable<List<String>> rows, Path path) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(path);
             CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("id", "name", "email"))) {
            for (List<String> row : rows) {
                printer.printRecord(row);
            }
        }
    }

    public void exportExcel(Iterable<List<String>> rows, Path path) throws IOException {
        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Users");
            int rowNum = 0;
            for (List<String> rowData : rows) {
                Row row = sheet.createRow(rowNum++);
                int colNum = 0;
                for (String cellData : rowData) {
                    row.createCell(colNum++).setCellValue(cellData);
                }
            }
            workbook.write(Files.newOutputStream(path));
        }
    }

    public void exportLargeExcel(Iterable<List<String>> rows, Path path) throws IOException {
        try (SXSSFWorkbook workbook = new SXSSFWorkbook(100)) {
            Sheet sheet = workbook.createSheet("Data");
            int rowNum = 0;
            for (List<String> rowData : rows) {
                Row row = sheet.createRow(rowNum++);
                int colNum = 0;
                for (String cellData : rowData) {
                    row.createCell(colNum++).setCellValue(cellData);
                }
            }
            workbook.write(Files.newOutputStream(path));
            workbook.dispose();
        }
    }

    public static String sanitizeCsvCell(String value) {
        if (value != null && !value.isEmpty() && "=+-@".indexOf(value.charAt(0)) >= 0) {
            return "'" + value;
        }
        return value;
    }

    public static void main(String[] args) throws IOException {
        List<List<String>> users = Arrays.asList(
            Arrays.asList("1", "Alice", "alice@example.com"),
            Arrays.asList("2", "Bob", "bob@example.com")
        );

        ExportExcel exporter = new ExportExcel();
        exporter.exportCsv(users, Paths.get("users.csv"));
        System.out.println("Wrote users.csv");

        exporter.exportExcel(users, Paths.get("users.xlsx"));
        System.out.println("Wrote users.xlsx");
    }
}
