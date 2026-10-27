# Dockerfile for a custom Lambda layer with compiled extensions
FROM public.ecr.aws/lambda/python:3.11

COPY requirements-layer.txt /tmp/
RUN pip install --target /opt/python -r /tmp/requirements-layer.txt

# Compile any native code
COPY src/ /opt/native/
RUN cd /opt/native && make install
