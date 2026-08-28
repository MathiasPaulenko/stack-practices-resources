"""Batch invoice generation with fpdf2."""
from fpdf import FPDF

invoices = [
    {"customer": "Acme", "amount": 1200, "id": 101},
    {"customer": "Globex", "amount": 850, "id": 102},
    {"customer": "Soylent", "amount": 2300, "id": 103},
]

for inv in invoices:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, txt=f"Invoice #{inv['id']}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Customer: {inv['customer']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, txt=f"Amount: ${inv['amount']}", new_x="LMARGIN", new_y="NEXT")
    pdf.output(f"invoice_{inv['id']}.pdf")

print(f"Created {len(invoices)} invoice PDFs")
