# Image Optimization — Companion Resources

Runnable helpers for the [image-optimization recipe](https://stackpractices.com/recipes/image-optimization/).

## Files

- `optimize_batch.py` — batch optimizer with two modes:
  - `--plan <dir>`: parses PNG/JPEG dimensions with stdlib only (no deps) and
    prints which responsive sizes would be generated per image.
  - `--run <dir>`: real optimization with Pillow — resize to responsive widths,
    WebP + JPEG fallback, EXIF stripped. Requires `pip install pillow`.

## Run

```bash
python optimize_batch.py --plan photos/          # works anywhere, no deps
python optimize_batch.py --run photos/           # needs Pillow
```

The `--plan` mode reads the image header directly (PNG `IHDR`, JPEG `SOF`
markers) so it works as a preview on any machine. Verified against a generated
4000x2000 PNG: it detects all four target sizes (320/640/1024/1920w).
