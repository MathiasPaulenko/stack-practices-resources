# Empaquetar Dependencias Python para Lambda — Archivos complementarios

Proyecto ejecutable complementario de la [receta de Lambda Layers](https://stackpractices.com/es/recipes/aws-lambda-python-dependencies/) en StackPractices.

- `manual-build.sh` / `docker-native-build.sh` — builds de layer para paquetes Python puros y con extensiones nativas.
- `build-layer.sh` — build automatizado: pip install en Docker (raíz del proyecto montada para que `requirements-layer.txt` sea visible), zip, publicación, ARN escrito en `layer-arn.txt`.
- `deploy-with-layer.sh` — zipear el código de función y adjuntar el ARN de layer publicado.
- `lambda_function.py` — handler de ejemplo importando desde la layer.
- `template.yaml` / `multi-layer-template.yaml` — configs SAM para setups de una y varias layers.
- `serverless.yml` — wiring de layers con Serverless Framework.
- `requirements.txt` — estrategia de split en dos archivos en un solo archivo.
- `arm64-build.sh` / `Dockerfile` / `strip-layer.sh` — build Graviton, imagen de layer para runtime personalizado y recorte del paquete.
