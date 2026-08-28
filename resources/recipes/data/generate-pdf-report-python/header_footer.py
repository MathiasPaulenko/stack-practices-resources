"""Header and footer with ReportLab."""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(2 * cm, 1 * cm, "StackPractices Report")
    canvas.drawRightString(
        A4[0] - 2 * cm,
        1 * cm,
        f"Page {doc.page}"
    )
    canvas.restoreState()


doc = SimpleDocTemplate("header_footer.pdf", pagesize=A4)
content = Paragraph("Content here", getSampleStyleSheet()["Normal"])
doc.build(
    [content],
    onFirstPage=add_header_footer,
    onLaterPages=add_header_footer
)
print("Created header_footer.pdf")
