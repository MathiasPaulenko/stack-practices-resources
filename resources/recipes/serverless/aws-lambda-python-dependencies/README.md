# Package Python Dependencies for AWS Lambda with Layers — Companion Files

Runnable companion for the [Lambda Layers recipe](https://stackpractices.com/recipes/aws-lambda-python-dependencies/) on StackPractices.

- `manual-build.sh` / `docker-native-build.sh` — layer builds for pure-Python and native-extension packages.
- `build-layer.sh` — automated build: Docker pip install (project root mounted so `requirements-layer.txt` is visible), zip, publish, ARN written to `layer-arn.txt`.
- `deploy-with-layer.sh` — zip function code and attach the published layer ARN.
- `lambda_function.py` — sample handler importing from the layer.
- `template.yaml` / `multi-layer-template.yaml` — SAM configs for single and split-layer setups.
- `serverless.yml` — Serverless Framework layer wiring.
- `requirements.txt` — the two-file split strategy in one file.
- `arm64-build.sh` / `Dockerfile` / `strip-layer.sh` — Graviton build, custom-runtime layer image, and package trimming.
