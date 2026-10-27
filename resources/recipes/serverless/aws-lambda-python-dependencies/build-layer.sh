#!/bin/bash
# build-layer.sh
set -euo pipefail

LAYER_NAME="app-deps"
RUNTIME="python3.11"
ARCH="x86_64"
REQUIREMENTS_FILE="requirements-layer.txt"

# Clean previous build
rm -rf build && mkdir -p build/python

# Install dependencies in Docker (matching Lambda runtime).
# Mount the project root so the requirements file is visible inside the container.
docker run --rm \
  -v "$PWD":/var/task \
  public.ecr.aws/lambda/python:${RUNTIME} \
  /bin/sh -c "pip install -r /var/task/${REQUIREMENTS_FILE} --target /var/task/build/python"

# Zip
cd build
zip -r "../${LAYER_NAME}.zip" python
cd ..

# Publish
LAYER_ARN=$(aws lambda publish-layer-version \
  --layer-name "${LAYER_NAME}" \
  --zip-file "fileb://${LAYER_NAME}.zip" \
  --compatible-runtimes "${RUNTIME}" \
  --compatible-architectures "${ARCH}" \
  --query 'LayerVersionArn' \
  --output text)

echo "Layer published: ${LAYER_ARN}"
echo "${LAYER_ARN}" > layer-arn.txt
