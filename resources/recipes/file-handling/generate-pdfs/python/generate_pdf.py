"""Generate a styled invoice PDF from an HTML template with WeasyPrint + Jinja2.

Metadata (title, author, subject, keywords) is declared in the HTML itself:
WeasyPrint maps <title> and the corresponding <meta> tags to the PDF
document properties automatically.

Usage:
    pip install -r requirements.txt
    python generate_pdf.py
"""

from weasyprint import HTML
from jinja2 import Template

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Invoice #{{ invoice_id }}</title>
  <meta name="author" content="ACME Inc.">
  <meta name="description" content="Payment due in 30 days">
  <meta name="keywords" content="invoice, acme, {{ invoice_id }}">
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
    h1 { color: #333; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
    .total { font-weight: bold; font-size: 1.2em; }
    @page { margin: 2cm; }
  </style>
</head>
<body>
  <h1>Invoice #{{ invoice_id }}</h1>
  <p>Customer: {{ customer }}</p>
  <table>
    <tr><th>Item</th><th>Qty</th><th>Price</th></tr>
    {% for item in items %}
    <tr><td>{{ item.name }}</td><td>{{ item.qty }}</td><td>${{ item.price }}</td></tr>
    {% endfor %}
  </table>
  <p class="total">Total: ${{ total }}</p>
</body>
</html>
"""


def generate_invoice(invoice_id: str, customer: str, items: list, total: str) -> str:
    """Render the invoice template and write it to disk. Returns the file path."""
    template = Template(HTML_TEMPLATE)
    html_out = template.render(
        invoice_id=invoice_id, customer=customer, items=items, total=total
    )
    output = f"invoice_{invoice_id}.pdf"
    HTML(string=html_out).write_pdf(output)
    return output


def generate_pdf_stream(html_content: str) -> bytes:
    """Generate a PDF as bytes without touching disk (Flask/FastAPI style)."""
    import io

    buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(buffer)
    return buffer.getvalue()


if __name__ == "__main__":
    path = generate_invoice(
        "12345",
        "Acme Corp",
        [
            {"name": "Consulting", "qty": 10, "price": "100.00"},
            {"name": "Support", "qty": 1, "price": "250.00"},
        ],
        "1,250.00",
    )
    print(f"Wrote {path}")
