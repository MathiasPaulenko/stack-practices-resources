# Azure Functions HTTP con Python — Archivos complementarios

Proyecto ejecutable complementario de la [receta de Azure Functions](https://stackpractices.com/es/recipes/azure-functions-python-http/) en StackPractices. Todos los archivos usan el modelo de programación Python v2 (decoradores, `function_app.py`).

- `function_app_http.py` — HTTP trigger GET/POST con códigos de estado correctos.
- `function_app_bindings.py` — bindings de entrada/salida de Cosmos DB.
- `function_app_async.py` — handler async con `aiohttp`.
- `function_app_services.py` — patrón singleton de servicio a nivel módulo.
- `function_app_errors.py` — middleware decorador `handle_errors`.
- `function_app_config.py` — lectura de App Settings / variables de entorno.
- `function_app_timer.py` — timer trigger NCRONTAB (¡seis campos!).
- `function_app_triggers.py` / `function_app_blob.py` — triggers de cola Service Bus y Blob Storage.
- `function_app_fastapi.py` — middleware ASGI envolviendo una app FastAPI.
- `local.settings.json` — plantilla de configuración de desarrollo (nunca commitear valores reales).
- `setup.sh` / `deploy.sh` — setup de Core Tools y despliegue con Azure CLI.
