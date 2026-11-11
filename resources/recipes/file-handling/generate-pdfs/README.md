# Generate PDFs — Runnable Examples

Companion code for the [Generate PDFs](https://stackpractices.com/recipes/generate-pdfs/) recipe on StackPractices.

Three parallel implementations of the same invoice: HTML template → PDF, in Python, Node.js, and Java.

## Structure

```
python/
  generate_pdf.py   WeasyPrint + Jinja2 invoice, streaming variant, HTML-driven metadata
  merge_pdfs.py     Merge PDFs with pypdf (the maintained PyPDF2 successor)
  requirements.txt
node/
  generate_pdf.js   Puppeteer + Handlebars invoice with timeouts and browser reuse
  package.json
java/
  PdfGenerator.java Thymeleaf + Flying Saucer (OpenPDF) HTML-to-PDF
```

## Python

```bash
cd python
pip install -r requirements.txt        # also needs system libs: libpango (apt install libpango-1.0-0 libpangoft2-1.0-0)
python generate_pdf.py                 # writes invoice_12345.pdf
python merge_pdfs.py a.pdf b.pdf out.pdf
```

## Node.js

```bash
cd node
npm install
npx puppeteer browsers install chrome
node generate_pdf.js                   # writes invoice_12345.pdf
```

## Java

`PdfGenerator.java` needs `org.thymeleaf:thymeleaf` and
`org.xhtmlrenderer:flying-saucer-pdf-openpdf` on the classpath, plus an
`invoice-template.html` in `src/main/resources`. Flying Saucer requires
well-formed XHTML — close all tags and quote all attributes.

## Production notes

- Reuse the Puppeteer browser instance; don't launch one per job.
- Enforce render timeouts — hostile or malformed HTML can hang a worker.
- iText is AGPL; OpenPDF/PDFBox are the free alternatives for closed source.
- Sanitize templates that touch user input: HTML-to-PDF engines fetch remote
  URLs, so untrusted HTML is an SSRF vector.
