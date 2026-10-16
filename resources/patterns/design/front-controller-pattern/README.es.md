# Patrón Front Controller — Archivos complementarios

Recursos complementarios del artículo
[Patrón Front Controller](https://stackpractices.com/es/patterns/front-controller-pattern/)
en StackPractices.

## Contenido

- `java/FrontControllerServlet.java` — forma canónica J2EE: un servlet mapeado a `/*` despacha a objetos `Command` que devuelven la vista.
- `php/index.php` — el bootstrap `index.php` que usa todo framework PHP (Symfony, Laravel); combínalo con una regla de rewrite que enrute todas las URLs aquí.
- `node/app.js` — Express como front controller: middleware para el preprocesamiento compartido, rutas como comandos.

## Ejecutar

```bash
# PHP (servidor embebido — toda petición llega a index.php)
php -S localhost:8080 php/index.php

# Node
cd node && npm install express && node app.js
curl -H "Authorization: Bearer valid" http://localhost:3000/user
```

Para Java, copia `FrontControllerServlet.java` a cualquier proyecto Jakarta/Servlet con vistas en `WEB-INF/views/`.

## Licencia

Libre para usar y adaptar bajo MIT. La atribución es bienvenida, no obligatoria.
