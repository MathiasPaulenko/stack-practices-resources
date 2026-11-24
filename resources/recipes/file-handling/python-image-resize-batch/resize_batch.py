"""Batch image resizer for the python-image-resize-batch recipe.

Usage:
    python resize_batch.py <input_dir> <output_dir> [options]

Resizes every supported image in <input_dir> (jpg, jpeg, png, webp) while
preserving aspect ratio, applies EXIF orientation, converts color modes as
needed, and writes results to <output_dir>. Supports JPEG and WebP output,
parallel processing, and a --dry-run mode that prints the plan without
writing anything.

Requires: pip install pillow
"""

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def process_one(args: tuple) -> tuple[str, str, str]:
    """Resize a single image. Returns (filename, status, detail)."""
    img_path, output_dir, max_size, out_format, quality = args
    try:
        from PIL import Image, ImageOps

        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)

        if img.mode == "CMYK":
            img = img.convert("RGB")

        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        stem = img_path.stem
        if out_format == "webp":
            if img.mode in ("P",):
                img = img.convert("RGBA")
            out_path = Path(output_dir) / f"{stem}.webp"
            img.save(out_path, "webp", quality=quality, method=6)
        else:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            out_path = Path(output_dir) / f"{stem}.jpg"
            img.save(
                out_path, "JPEG", quality=quality, optimize=True, progressive=True
            )

        return img_path.name, "ok", f"{out_path.name} ({img.size[0]}x{img.size[1]})"
    except Exception as exc:  # noqa: BLE001 - batch job, report and continue
        return img_path.name, "error", str(exc)


def collect_images(input_dir: Path) -> list[Path]:
    return sorted(
        p for p in input_dir.glob("*") if p.suffix.lower() in EXTENSIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--max-size", type=int, default=1200,
                        help="Max width/height in pixels (default: 1200)")
    parser.add_argument("--format", choices=["jpeg", "webp"], default="webp",
                        help="Output format (default: webp)")
    parser.add_argument("--quality", type=int, default=85,
                        help="Encoding quality 0-100 (default: 85)")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel worker processes (default: 1)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without processing")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"error: {args.input_dir} is not a directory", file=sys.stderr)
        return 2

    files = collect_images(args.input_dir)
    if not files:
        print("no images found")
        return 0

    print(f"{len(files)} image(s) -> {args.output_dir} "
          f"(max {args.max_size}px, {args.format}, q={args.quality})")

    if args.dry_run:
        for f in files:
            print(f"  {f.name}")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        (f, args.output_dir, args.max_size, args.format, args.quality)
        for f in files
    ]

    errors = 0
    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(process_one, t) for t in tasks]
            for i, future in enumerate(as_completed(futures), 1):
                name, status, detail = future.result()
                if status != "ok":
                    errors += 1
                print(f"[{i}/{len(tasks)}] {status}: {name} -> {detail}")
    else:
        for i, t in enumerate(tasks, 1):
            name, status, detail = process_one(t)
            if status != "ok":
                errors += 1
            print(f"[{i}/{len(tasks)}] {status}: {name} -> {detail}")

    print(f"done: {len(tasks) - errors} ok, {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
