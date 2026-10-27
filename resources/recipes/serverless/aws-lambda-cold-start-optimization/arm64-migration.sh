# Update function architecture
aws lambda update-function-configuration \
  --function-name my-api \
  --architectures arm64

# Rebuild layer for ARM64
docker run --rm --platform linux/arm64 \
  -v "$PWD/layer":/var/task \
  public.ecr.aws/lambda/python:3.11-arm64 \
  /bin/sh -c "pip install -r requirements.txt --target /var/task/python"
