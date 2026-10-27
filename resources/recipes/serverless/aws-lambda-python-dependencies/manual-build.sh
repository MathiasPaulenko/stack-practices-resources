# Create a directory structure matching Lambda's Python path
mkdir -p layer/python
pip install requests pydantic sqlalchemy --target layer/python

# Zip the layer
cd layer
zip -r ../my-deps-layer.zip python
cd ..

# Publish the layer
aws lambda publish-layer-version \
  --layer-name my-python-deps \
  --zip-file fileb://my-deps-layer.zip \
  --compatible-runtimes python3.11 python3.12 \
  --compatible-architectures x86_64 arm64
