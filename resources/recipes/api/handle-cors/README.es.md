# Configurar CORS en Express, Flask y Spring Boot

Recurso complementario de [Configurar CORS en Express, Flask y Spring Boot](https://stackpractices.com/es/recipes/handle-cors/).

## Archivos

- `cors_server.py` — API Flask con middleware CORS de lista de orígenes y manejo de preflight OPTIONS.
- `cors-server.mjs` — el mismo middleware para Express (Node.js).
- `verify-cors.sh` — script curl que verifica peticiones simples, preflight y orígenes no permitidos.
- `requirements.txt`, `package.json` — dependencias.

## Uso

```bash
# Python
pip install -r requirements.txt
python cors_server.py

# o Node.js
npm install
node cors-server.mjs

# Después, desde otra terminal:
bash verify-cors.sh http://localhost:5000
```

## Qué demuestra

- Reflejar solo orígenes de la lista en `Access-Control-Allow-Origin`.
- Respuestas de preflight (`OPTIONS`) con métodos, encabezados permitidos y `Max-Age`.
- Soporte de credenciales (`Access-Control-Allow-Credentials: true`) sin el comodín `*`.
- `Vary: Origin` en las respuestas para que las cachés compartidas no mezclen orígenes.
