# Optimización de Imágenes — Recursos Complementarios

Helpers ejecutables para la [receta image-optimization](https://stackpractices.com/es/recipes/image-optimization/).

## Archivos

- `optimize_batch.py` — optimizador por lotes con dos modos:
  - `--plan <dir>`: lee dimensiones PNG/JPEG solo con stdlib (sin deps) e
    imprime qué tamaños responsive se generarían por imagen.
  - `--run <dir>`: optimización real con Pillow — resize a anchos responsive,
    fallback WebP + JPEG, EXIF eliminado. Requiere `pip install pillow`.

## Ejecutar

```bash
python optimize_batch.py --plan fotos/          # funciona en cualquier lado, sin deps
python optimize_batch.py --run fotos/           # necesita Pillow
```

El modo `--plan` lee el header de la imagen directamente (`IHDR` en PNG,
marcadores `SOF` en JPEG), así que sirve como preview en cualquier máquina.
Verificado contra un PNG generado de 4000x2000: detecta los cuatro tamaños
objetivo (320/640/1024/1920w).
