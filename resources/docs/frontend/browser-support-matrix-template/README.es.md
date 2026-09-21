# Matriz de Soporte de Navegadores — Recursos complementarios

Archivos complementarios de la [Plantilla de Matriz de Soporte de Navegadores](https://stackpractices.com/es/docs/browser-support-matrix-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `browser-support-matrix.md` | Markdown | La matriz rellenable: niveles de soporte, compatibilidad de funciones (JS / CSS / APIs Web), estrategia de polyfills, fallbacks, matriz de pruebas, configuración de build, política de banner |
| `feature-matrix.json` | JSON | Versión legible por máquina de la matriz de funciones — niveles más soporte/polyfill/fallback por función para tooling o dashboards |
| `babel.config.js` | JavaScript | Targets de `@babel/preset-env` acordes a la línea base de la matriz, con `useBuiltIns: 'usage'` |
| `browserslist` | Config | Browserslist de producción/desarrollo — la fuente única de verdad que mueve Babel, Autoprefixer y ESLint |
| `upgrade-banner.html` | HTML | Banner de actualización con prueba de función para navegadores bajo la línea base (sin UA sniffing) |

## Inicio rápido

### 1. Fija la línea base desde la analítica

Extrae el tráfico por navegador/versión de los últimos 90 días. Elige un umbral de uso (habitual: >0.5% para Nivel 1, >0.1% para Nivel 2) y asigna niveles mecánicamente.

### 2. Sincroniza los archivos de configuración

Copia `browserslist` a la raíz de tu repo y mantén los targets de `babel.config.js` alineados — la configuración aplica la matriz, el documento la refleja.

### 3. Rellena la matriz de funciones

Lista solo las funciones que tu app usa de verdad (o usará en los próximos dos trimestres). Cada hueco se resuelve en exactamente un resultado: un polyfill con coste gzipped medido, o un fallback.

### 4. Conecta el banner

Incluye `upgrade-banner.html` en tu layout base. La prueba de función (structuredClone/fetch/lazy-loading) marca cualquier navegador bajo la línea base sin parsear user agents.

## Revisa trimestralmente

Comprueba la analítica por cruces de umbral, caniuse por soportes recién publicados, y re-ejecuta los smoke tests de Nivel 2. La línea base `last 2 versions` de Browserslist se mueve cada ~6 semanas actualices el documento o no.
