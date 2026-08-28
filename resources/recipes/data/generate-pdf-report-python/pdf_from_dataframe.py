"""PDF from a pandas DataFrame."""
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Create sample data
rows = [
    {"region": "North", "orders": 82, "revenue": 5210},
    {"region": "South", "orders": 65, "revenue": 4180},
    {"region": "East", "orders": 100, "revenue": 6040},
]
df = pd.DataFrame(rows)
df_summary = df.groupby("region")[["orders", "revenue"]].sum().reset_index()

table_data = [df_summary.columns.tolist()] + df_summary.values.tolist()

doc = SimpleDocTemplate("sales_summary.pdf", pagesize=A4)
table = Table(table_data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a56db")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))
doc.build([table])
print("Created sales_summary.pdf")
