"""PDF with a matplotlib chart embedded."""
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import cm

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(["North", "South", "East"], [5210, 4180, 6040])
ax.set_title("Revenue by Region")
fig.savefig("chart.png", format="png", bbox_inches="tight")
plt.close(fig)

doc = SimpleDocTemplate("report_with_chart.pdf", pagesize=A4)
img = Image("chart.png", width=15 * cm, height=7 * cm)
doc.build([img, Spacer(1, 1 * cm)])
print("Created report_with_chart.pdf")
