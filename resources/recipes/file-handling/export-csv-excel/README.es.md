# Exportar Datos a CSV y Excel — Companion

Repositorio companion para la [receta Exportar Datos a CSV y Excel](https://stackpractices.com/es/recipes/export-csv-excel/).

## Contenido

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `export_csv.py` | Python | Exportación CSV/Excel con pandas, streaming, ZIP y fórmulas |
| `sanitize_csv.py` | Python | Utilidades de sanitización CSV injection con tests |
| `export_excel.js` | JavaScript | Exportación CSV/Excel con fast-csv, xlsx y endpoint Express streaming |
| `ExportExcel.java` | Java | Exportación CSV/Excel con Apache Commons CSV y POI (incl. SXSSF) |
| `requirements.txt` | Python | Dependencias |
| `package.json` | Node.js | Dependencias |
| `pom.xml` | Java | Dependencias Maven |

## Inicio Rápido

### Python

```bash
pip install -r requirements.txt
python export_csv.py
python sanitize_csv.py  # ejecutar tests de sanitización
```

### JavaScript

```bash
npm install
node export_excel.js
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="ExportExcel"
```

## Características Clave

- **Exportación en memoria**: pandas `to_csv`, SheetJS `XLSX.writeFile`, Apache POI `XSSFWorkbook`
- **Exportación streaming**: Python `csv.writer` con generador, Node.js `fast-csv` pipe, Java `SXSSFWorkbook` con ventana deslizante
- **Sanitización CSV injection**: Prefijar `=`, `+`, `-`, `@` con comilla simple
- **Endpoint Express**: CSV streaming con manejo de errores y abort signal
- **Excel multi-hoja**: pandas `ExcelWriter` con motor `openpyxl`
- **Exportación ZIP**: Múltiples archivos CSV como un solo archivo ZIP
- **Fórmulas Excel**: `openpyxl` escritura de fórmulas con `=SUM()`
