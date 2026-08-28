"""Generate a PDF from HTML and CSS using WeasyPrint."""
from weasyprint import HTML, CSS

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Helvetica, sans-serif; margin: 2cm; }
        h1 { color: #1a56db; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #1a56db; color: white; }
    </style>
</head>
<body>
    <h1>Monthly Sales Report</h1>
    <table>
        <tr><th>Region</th><th>Orders</th><th>Revenue</th></tr>
        <tr><td>North</td><td>82</td><td>$5,210</td></tr>
        <tr><td>South</td><td>65</td><td>$4,180</td></tr>
        <tr><td>East</td><td>100</td><td>$6,040</td></tr>
    </table>
</body>
</html>
"""

HTML(string=html_content).write_pdf("report_from_html.pdf")
print("Created report_from_html.pdf")
