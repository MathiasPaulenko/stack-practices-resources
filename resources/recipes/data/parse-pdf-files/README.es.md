# Extraer Texto de PDFs en Python, JavaScript y Java

Recurso complementario de [Extraer Texto de PDFs en Python, JavaScript y Java](https://stackpractices.com/es/recipes/parse-pdf-files/).

## Archivos

- `pdf_examples.py` — ejemplos en Python (pypdf, pdfplumber, pikepdf) ejecutables como comandos independientes.
- `pdf_examples.mjs` — ejemplos en Node.js (pdf-parse, pdf-lib).
- `requirements.txt` — dependencias de Python.
- `package.json` — dependencias de Node.js.

## Uso

```bash
pip install -r requirements.txt
python pdf_examples.py sample      # crea sample.pdf primero
python pdf_examples.py text
python pdf_examples.py metadata
python pdf_examples.py tables
python pdf_examples.py encrypted

npm install
node pdf_examples.mjs text         # requiere el sample.pdf del paso anterior
node pdf_examples.mjs metadata
```

## Ejemplos

| Comando | Descripción |
|---------|-------------|
| `sample` | Crea `sample.pdf` con texto y una tabla (ejecutar primero) |
| `text` | Extrae texto página a página con `pypdf` |
| `metadata` | Lee la información del documento y escribe un campo `Producer` actualizado |
| `tables` | Extrae la tabla de la página 2 y coordenadas de palabras con `pdfplumber` |
| `encrypted` | Cifra una copia con `pikepdf` y luego la descifra y analiza |
| `text` (mjs) | Extrae texto con `pdf-parse` en Node.js |
| `metadata` (mjs) | Lee título/autor con `pdf-lib` en Node.js |
