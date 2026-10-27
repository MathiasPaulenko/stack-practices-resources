# Build in a container matching Lambda's runtime
docker run --rm -v "$PWD/layer":/var/task public.ecr.aws/lambda/python:3.11 \
  /bin/sh -c "pip install numpy pandas psycopg2-binary --target /var/task/python"

# Zip and publish
cd layer
zip -r ../native-deps-layer.zip python
cd ..

aws lambda publish-layer-version \
  --layer-name native-python-deps \
  --zip-file fileb://native-deps-layer.zip \
  --compatible-runtimes python3.11 \
  --compatible-architectures x86_64
