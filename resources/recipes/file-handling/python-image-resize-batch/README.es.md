# Redimensionar Imágenes en Lote con Python — Recursos Complementarios

CLI ejecutable de la [receta python-image-resize-batch](https://stackpractices.com/es/recipes/python-image-resize-batch/).

## Archivos

- `resize_batch.py` — redimensionador batch con CLI real:
  - Explora un directorio buscando `jpg`/`jpeg`/`png`/`webp`.
  - Aplica la orientación EXIF (`ImageOps.exif_transpose`) antes de redimensionar.
  - Preserva el aspect ratio con `thumbnail()` — nunca agranda.
  - Convierte modos `RGBA`/`P`/`CMYK` para salida JPEG, o conserva el alfa en WebP.
  - Multiprocessing opcional (`--workers`) y vista previa con `--dry-run`.

## Uso

```bash
pip install pillow

python resize_batch.py photos/ out/                      # WebP, máx. 1200px
python resize_batch.py photos/ out/ --format jpeg        # JPEG progresivo
python resize_batch.py photos/ out/ --max-size 800 --quality 80
python resize_batch.py photos/ out/ --workers 4          # en paralelo
python resize_batch.py photos/ out/ --dry-run            # solo listar
```

Sale con código distinto de cero si alguna imagen falla, así que encaja directo en pipelines de CI.
