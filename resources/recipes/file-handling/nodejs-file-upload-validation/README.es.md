# Validación de Subidas en Node.js — Recursos complementarios

Código ejecutable referenciado en
[Validación de Subidas en Node.js: Tipo, Tamaño y Contenido](https://stackpractices.com/es/recipes/nodejs-file-upload-validation/).

| Archivo | Propósito |
| --- | --- |
| `upload.js` | Pipeline completo en Express: límites de tamaño/cantidad, filtro de extensión + MIME, verificación de firma con `file-type`, middleware de errores |
| `avatar.js` | `memoryStorage` + Sharp: límites de dimensiones, resize, limpieza de EXIF vía re-encode |

Los dos archivos son apps autocontenidas — instala `express multer@^2 file-type`
(más `sharp` para `avatar.js`) y ejecútalos con `node <archivo>.js`. Requiere
multer 2.x; la rama 1.x deprecada arrastra vulnerabilidades conocidas.

La validación corre por capas — límites y filtros primero (barato), verificación
de contenido al final. Nunca confíes en una sola verificación.
