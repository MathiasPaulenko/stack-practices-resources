# Batch Resize Images with Python — Companion Resources

Runnable CLI for the [python-image-resize-batch recipe](https://stackpractices.com/recipes/python-image-resize-batch/).

## Files

- `resize_batch.py` — batch resizer with a real CLI:
  - Scans a directory for `jpg`/`jpeg`/`png`/`webp` files.
  - Applies EXIF orientation (`ImageOps.exif_transpose`) before resizing.
  - Preserves aspect ratio via `thumbnail()` — never upscales.
  - Converts `RGBA`/`P`/`CMYK` modes for JPEG output, or keeps alpha for WebP.
  - Optional multiprocessing (`--workers`) and `--dry-run` preview.

## Run

```bash
pip install pillow

python resize_batch.py photos/ out/                      # WebP, max 1200px
python resize_batch.py photos/ out/ --format jpeg        # progressive JPEG
python resize_batch.py photos/ out/ --max-size 800 --quality 80
python resize_batch.py photos/ out/ --workers 4          # parallel
python resize_batch.py photos/ out/ --dry-run            # list only
```

Exits non-zero if any image fails, so it drops cleanly into CI pipelines.
