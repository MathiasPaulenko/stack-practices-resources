"""Basic PDF with fpdf2."""
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

pdf.cell(200, 10, txt="Sales Report", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(10)

pdf.cell(200, 10, txt="Total Revenue: $15,430", new_x="LMARGIN", new_y="NEXT")
pdf.cell(200, 10, txt="Orders: 247", new_x="LMARGIN", new_y="NEXT")

pdf.output("report.pdf")
print("Created report.pdf")
