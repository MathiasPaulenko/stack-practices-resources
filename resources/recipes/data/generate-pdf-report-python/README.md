# Generate PDF Reports in Python — Companion Resources

Runnable examples for the [Generate PDF Reports in Python](https://stackpractices.com/recipes/generate-pdf-report-python/) recipe.

## Files

| File                  | Description                                          |
| --------------------- | ---------------------------------------------------- |
| `basic_fpdf2.py`      | Simple text PDF with fpdf2                           |
| `styled_reportlab.py` | Styled table and title with ReportLab                |
| `pdf_from_dataframe.py` | Render a pandas DataFrame to PDF                   |
| `header_footer.py`    | Page numbers and footer text with ReportLab          |
| `chart_report.py`     | Embed a matplotlib chart into a PDF                  |
| `weasyprint_html.py`  | Convert HTML and CSS to PDF with WeasyPrint          |
| `batch_invoices.py`   | Generate multiple PDFs from a list of records        |
| `requirements.txt`    | Python dependencies                                  |
| `README.md`           | English instructions                                 |
| `README.es.md`        | Spanish instructions                                 |

## Quick Start

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

python basic_fpdf2.py
python styled_reportlab.py
python pdf_from_dataframe.py
python header_footer.py
python chart_report.py
python weasyprint_html.py
python batch_invoices.py
```

## Notes

- fpdf2 is great for simple text PDFs.
- ReportLab is better for tables, headers, footers, and styled multi-page reports.
- WeasyPrint is the easiest path when the report already exists as HTML and CSS.
