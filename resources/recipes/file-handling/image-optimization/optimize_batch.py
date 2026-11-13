"""Batch image optimizer for the image-optimization recipe.

Two modes:
    python optimize_batch.py --plan photos/     # resize plan, no deps needed
    python optimize_batch.py --run photos/      # real optimization (Pillow)

--plan reads image headers (PNG/JPEG dimensions via stdlib struct parsing)
and prints which sizes would be generated. --run resizes + transcodes to
WebP with a JPEG fallback and strips EXIF metadata.
"""

import argparse
import struct
import sys
from pathlib import Path

SIZES = [320, 640, 1024, 1920]


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h
    except OSError:
        pass
    return None


def jpeg_size(path: Path) -> tuple[int, int] | None:
    try:
        with open(path, "rb") as f:
            data = f.read()
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5 : i + 9])
                return w, h
            length = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + length
    except OSError:
        pass
    return None


def image_size(path: Path) -> tuple[int, int] | None:
    return png_size(path) or jpeg_size(path)


def plan(directory: Path) -> None:
    images = sorted(directory.glob("*.png")) + sorted(directory.glob("*.jp*g"))
    if not images:
        print(f"No PNG/JPEG files in {directory}")
        return
    for img in images:
        size = image_size(img)
        if not size:
            print(f"{img.name}: could not read dimensions, skipping")
            continue
        w, h = size
        targets = [s for s in SIZES if s < w]
        print(f"{img.name} ({w}x{h}) -> sizes {[f'{s}w' for s in targets]} + webp/jpeg fallback")
    print(f"\n{len(images)} image(s) planned. Run with --run to optimize (needs Pillow).")


def run(directory: Path, quality: int) -> None:
    from PIL import Image

    out = directory / "optimized"
    out.mkdir(exist_ok=True)
    images = sorted(directory.glob("*.png")) + sorted(directory.glob("*.jp*g"))
    for img_path in images:
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            for width in SIZES:
                if img.width <= width:
                    continue
                ratio = width / img.width
                resized = img.resize((width, int(img.height * ratio)), Image.Resampling.LANCZOS)
                resized.save(out / f"{img_path.stem}-{width}.webp", "WEBP", quality=quality)
                resized.save(out / f"{img_path.stem}-{width}.jpg", "JPEG", quality=quality)
        print(f"{img_path.name}: done")
    print(f"Optimized files in {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plan", action="store_true")
    group.add_argument("--run", action="store_true")
    parser.add_argument("--quality", type=int, default=80)
    args = parser.parse_args()

    if args.plan:
        plan(args.directory)
    else:
        try:
            run(args.directory, args.quality)
        except ImportError:
            sys.exit("Pillow required for --run: pip install pillow")
