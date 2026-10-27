# Build for ARM64 (Graviton2 — lower cost, better performance)
docker run --rm --platform linux/arm64 \
  -v "$PWD/layer":/var/task \
  public.ecr.aws/lambda/python:3.11-arm64 \
  /bin/sh -c "pip install numpy --target /var/task/python"

aws lambda publish-layer-version \
  --layer-name native-deps-arm64 \
  --zip-file fileb://native-deps-layer.zip \
  --compatible-runtimes python3.11 \
  --compatible-architectures arm64
