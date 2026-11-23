# Patrón Page Controller — Archivos complementarios

Archivos complementarios del [Patrón Page Controller](https://stackpractices.com/es/patterns/page-controller-pattern/) en StackPractices.

## Contenido

- `page_controller.py` — ejemplo ejecutable: `Request`/`Response`, tres controladores de página y el mapa plano ruta→controlador. Ejecútalo: `python page_controller.py`.
- `test_page_controller.py` — suite de pytest que cubre routing, manejo de parámetros, un 404 y lógica de página. Ejecútala: `pytest test_page_controller.py`.

## Qué mirar

- Cada controlador es dueño de una página de extremo a extremo — nada compartido entre ellos.
- `CONTROLLERS` es toda la historia del routing: añadir una página es una clase + una entrada. Cuando el mapa necesita patrones, middleware o preprocesamiento compartido, ese es el umbral del Front Controller.
- `test_route_map_stays_declarative` vigila el propio mapa — una fuente común de 404 silenciosos.
