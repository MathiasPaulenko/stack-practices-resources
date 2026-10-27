# HTTP-Triggered Azure Functions in Python — Companion Files

Runnable companion for the [Azure Functions recipe](https://stackpractices.com/recipes/azure-functions-python-http/) on StackPractices. All files target the Python v2 programming model (decorators, `function_app.py`).

- `function_app_http.py` — GET/POST HTTP trigger with proper status codes.
- `function_app_bindings.py` — Cosmos DB input/output bindings.
- `function_app_async.py` — async handler with `aiohttp`.
- `function_app_services.py` — module-level service singleton pattern.
- `function_app_errors.py` — `handle_errors` decorator middleware.
- `function_app_config.py` — reading App Settings / env vars.
- `function_app_timer.py` — NCRONTAB timer trigger (six fields!).
- `function_app_triggers.py` / `function_app_blob.py` — Service Bus queue and Blob Storage triggers.
- `function_app_fastapi.py` — ASGI middleware wrapping a FastAPI app.
- `local.settings.json` — development settings template (never commit real values).
- `setup.sh` / `deploy.sh` — Core Tools setup and Azure CLI deployment.
