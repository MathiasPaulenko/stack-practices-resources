"""Merge multiple PDF files into one using pypdf.

pypdf is the maintained successor of the deprecated PyPDF2 package.

Usage:
    pip install -r requirements.txt
    python merge_pdfs.py page1.pdf page2.pdf combined.pdf
"""

import sys

from pypdf import PdfWriter


def merge_pdfs(pdf_paths: list[str], output_path: str) -> None:
    """Merge multiple PDF files into one."""
    merger = PdfWriter()
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    with open(output_path, "wb") as out:
        merger.write(out)
    merger.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python merge_pdfs.py <in1.pdf> <in2.pdf> [more...] <out.pdf>")
    *inputs, output = sys.argv[1:]
    merge_pdfs(inputs, output)
    print(f"Merged {len(inputs)} files into {output}")
