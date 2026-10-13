# Analizar Archivos Excel en Python, JavaScript y Java

Recurso complementario de [Analizar Archivos Excel en Python, JavaScript y Java](https://stackpractices.com/es/recipes/parse-excel-files/).

## Archivos

- `excel_parse.py` — ejemplos con openpyxl: crear, leer, escribir y hacer streaming de un libro grande.
- `excel_parse.mjs` — ejemplos con SheetJS (`xlsx`) para Node.js: crear, leer, escribir.
- `ExcelParser.java` — ejemplo con Apache POI: leer la primera hoja de un libro.
- `requirements.txt` — dependencias de Python.
- `package.json` — dependencias de Node.js.

## Uso

### Python

```bash
pip install -r requirements.txt
python excel_parse.py sample   # crea sample.xlsx (ejecutar primero)
python excel_parse.py read
python excel_parse.py write
python excel_parse.py large    # lectura en streaming con read_only=True
```

### Node.js

```bash
npm install
node excel_parse.mjs sample    # crea sample.xlsx (ejecutar primero)
node excel_parse.mjs read
node excel_parse.mjs write
```

### Java

```bash
# Compila con poi-ooxml 5.3.0 en el classpath, luego:
java ExcelParser sample.xlsx
```

## Notas

- `excel_parse.py large` demuestra `read_only=True`, que entrega filas en streaming en lugar de cargar todo el libro — el modo correcto para archivos que no caben cómodamente en RAM.
- El ejemplo Java necesita `org.apache.poi:poi-ooxml` en el classpath; mira el fragmento Maven en la receta.
