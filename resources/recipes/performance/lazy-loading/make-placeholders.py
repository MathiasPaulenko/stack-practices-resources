"""Generate SVG placeholder images for the lazy-loading demo.

Creates images/img-0.svg .. images/img-11.svg plus images/fallback.svg
so index.html runs fully offline — no external image service needed.

Usage: python make-placeholders.py
"""

from pathlib import Path

OUT = Path(__file__).parent / "images"

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360">
  <rect width="640" height="360" fill="{bg}"/>
  <text x="320" y="180" font-family="system-ui, sans-serif" font-size="42"
        font-weight="600" fill="#f1f5f9" text-anchor="middle"
        dominant-baseline="middle">Image {n}</text>
</svg>
"""

COLORS = [
    "#0f766e", "#0e7490", "#1d4ed8", "#6d28d9", "#a21caf", "#be185d",
    "#b91c1c", "#c2410c", "#a16207", "#4d7c0f", "#15803d", "#0f766e",
]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for i in range(12):
        (OUT / f"img-{i}.svg").write_text(
            TEMPLATE.format(bg=COLORS[i], n=i), encoding="utf-8"
        )
    (OUT / "fallback.svg").write_text(
        TEMPLATE.format(bg="#475569", n="missing"), encoding="utf-8"
    )
    print(f"Wrote {13} placeholders to {OUT}")


if __name__ == "__main__":
    main()
