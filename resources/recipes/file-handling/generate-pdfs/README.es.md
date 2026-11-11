# Generar PDFs — Ejemplos ejecutables

Código complementario de la receta [Generar PDFs](https://stackpractices.com/es/recipes/generate-pdfs/) en StackPractices.

Tres implementaciones paralelas de la misma factura: plantilla HTML → PDF, en Python, Node.js y Java.

## Estructura

```
python/
  generate_pdf.py   Factura con WeasyPrint + Jinja2, variante streaming, metadata vía HTML
  merge_pdfs.py     Fusión de PDFs con pypdf (sucesor mantenido de PyPDF2)
  requirements.txt
node/
  generate_pdf.js   Factura con Puppeteer + Handlebars, con timeouts y reutilización del navegador
  package.json
java/
  PdfGenerator.java HTML-a-PDF con Thymeleaf + Flying Saucer (OpenPDF)
```

## Python

```bash
cd python
pip install -r requirements.txt        # también requiere libs del sistema: libpango (apt install libpango-1.0-0 libpangoft2-1.0-0)
python generate_pdf.py                 # escribe invoice_12345.pdf
python merge_pdfs.py a.pdf b.pdf out.pdf
```

## Node.js

```bash
cd node
npm install
npx puppeteer browsers install chrome
node generate_pdf.js                   # escribe invoice_12345.pdf
```

## Java

`PdfGenerator.java` necesita `org.thymeleaf:thymeleaf` y
`org.xhtmlrenderer:flying-saucer-pdf-openpdf` en el classpath, más un
`invoice-template.html` en `src/main/resources`. Flying Saucer requiere
XHTML bien formado — cierra todas las etiquetas y entrecomilla los atributos.

## Notas de producción

- Reutiliza la instancia del navegador en Puppeteer; no lances una por trabajo.
- Impone timeouts de renderizado — un HTML hostil o malformado puede colgar un worker.
- iText es AGPL; OpenPDF/PDFBox son las alternativas libres para código cerrado.
- Sanitiza las plantillas que toquen input del usuario: los motores HTML-a-PDF
  descargan URLs remotas, así que HTML no confiable es un vector SSRF.
