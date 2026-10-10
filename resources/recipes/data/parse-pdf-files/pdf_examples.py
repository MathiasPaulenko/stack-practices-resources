"""Runnable examples for the "Parse PDF Files" recipe.

Usage:
    python pdf_examples.py <example>

Examples:
    sample      Create sample.pdf with text and a table (run this first)
    text        Extract text page by page with pypdf
    metadata    Read and update document metadata with pypdf
    tables      Extract tables and positioned words with pdfplumber
    encrypted   Encrypt a copy, then decrypt and parse it with pikepdf
"""

import sys
from pathlib import Path

SAMPLE = "sample.pdf"


def sample() -> None:
    """Create sample.pdf: page 1 with text lines, page 2 with a simple table."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_title("Quarterly Sales Report")
    pdf.set_author("StackPractices Demo")
    pdf.add_page()
    pdf.set_font("helvetica", size=16)
    pdf.cell(text="Quarterly Sales Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    for line in [
        "Total revenue grew 12% year over year.",
        "The EMEA region contributed 41% of sales.",
        "Refunds stayed below the 2% threshold.",
    ]:
        pdf.cell(text=line, new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(text="Sales by region", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    rows = [
        ("Region", "Revenue", "Growth"),
        ("EMEA", "1,240,000", "9%"),
        ("Americas", "1,780,000", "14%"),
        ("APAC", "620,000", "18%"),
    ]
    for row in rows:
        for cell in row:
            pdf.cell(40, 8, text=cell, border=1)
        pdf.ln()
    pdf.output(SAMPLE)
    print(f"Wrote {SAMPLE}")


def text(path: str = SAMPLE) -> None:
    from pypdf import PdfReader

    reader = PdfReader(path)
    print(f"Pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages, start=1):
        print(f"--- page {i} ---")
        print(page.extract_text())


def metadata(path: str = SAMPLE) -> None:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(path)
    meta = reader.metadata
    print("Title:", meta.title)
    print("Author:", meta.author)
    print("Created:", meta.creation_date)

    writer = PdfWriter(clone_from=reader)
    writer.add_metadata({"/Producer": "pdf_examples.py"})
    out = Path(path).with_suffix(".tagged.pdf")
    with open(out, "wb") as f:
        writer.write(f)
    print(f"Wrote {out} with updated Producer")


def tables(path: str = SAMPLE) -> None:
    import pdfplumber

    with pdfplumber.open(path) as pdf:
        page = pdf.pages[1]
        for table in page.extract_tables():
            for row in table:
                print(row)

        words = pdf.pages[0].extract_words()[:8]
        print("\nFirst words with coordinates:")
        for w in words:
            print(f"  {w['text']!r} at x0={w['x0']:.0f} top={w['top']:.0f}")


def encrypted(path: str = SAMPLE) -> None:
    import pikepdf

    locked = Path(path).with_suffix(".locked.pdf")
    with pikepdf.open(path) as pdf:
        pdf.save(locked, encryption=pikepdf.Encryption(user="demo", owner="demo"))
    print(f"Wrote {locked}")

    with pikepdf.open(locked, password="demo") as pdf:
        unlocked = Path(path).with_suffix(".unlocked.pdf")
        pdf.save(unlocked)
    print(f"Wrote {unlocked} — now readable by pypdf/pdfplumber")

    text(str(unlocked))


EXAMPLES = {
    "sample": sample,
    "text": text,
    "metadata": metadata,
    "tables": tables,
    "encrypted": encrypted,
}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if name not in EXAMPLES:
        print(f"Unknown example {name!r}. Choose from: {', '.join(EXAMPLES)}")
        sys.exit(1)
    EXAMPLES[name]()
