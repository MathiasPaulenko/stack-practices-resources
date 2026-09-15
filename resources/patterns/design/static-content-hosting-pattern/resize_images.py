"""Generate responsive image variants for srcset."""

from PIL import Image
from pathlib import Path


VARIANTS = {
    "thumbnail": (150, 150),
    "small": (320, 240),
    "medium": (640, 480),
    "large": (1024, 768),
    "xlarge": (1920, 1440),
}


def resize_image(input_path, output_dir, variants=None):
    """Generate resized variants of an image.

    Args:
        input_path: path to the source image.
        output_dir: directory to write variants into.
        variants: dict of variant name to (width, height). Defaults to VARIANTS.

    Returns:
        Dict mapping variant name to output file path.
    """
    variants = variants or VARIANTS
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(input_path)
    source = source.convert("RGB")
    stem = Path(input_path).stem
    ext = Path(input_path).suffix or ".jpg"

    outputs = {}
    for name, (width, height) in variants.items():
        resized = source.copy()
        resized.thumbnail((width, height), Image.LANCZOS)
        out_path = output_dir / f"{stem}_{name}{ext}"
        resized.save(out_path, quality=85, optimize=True)
        outputs[name] = str(out_path)

    return outputs


def generate_srcset(input_path, cdn_base, variants=None):
    """Generate an srcset attribute string for a CDN-hosted image.

    Args:
        input_path: path to the source image (used to read dimensions).
        cdn_base: CDN URL prefix (e.g. "https://cdn.example.com/images").
        variants: dict of variant name to (width, height). Defaults to VARIANTS.

    Returns:
        srcset string like "url 150w, url 320w, ..."
    """
    variants = variants or VARIANTS
    stem = Path(input_path).stem
    ext = Path(input_path).suffix or ".jpg"

    parts = []
    for name, (width, _) in variants.items():
        url = f"{cdn_base}/{stem}_{name}{ext}"
        parts.append(f"{url} {width}w")

    return ", ".join(parts)


if __name__ == "__main__":
    outputs = resize_image("source.jpg", "dist/images")
    for name, path in outputs.items():
        print(f"  {name}: {path}")

    srcset = generate_srcset("source.jpg", "https://cdn.example.com/images")
    print(f"srcset: {srcset}")
