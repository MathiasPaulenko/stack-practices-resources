# Contribuir a [Nombre del Proyecto]

¡Gracias por tu interés en contribuir! Este documento explica cómo
reportar bugs, sugerir funcionalidades y enviar cambios.

## Tabla de contenidos

- [Formas de contribuir](#formas-de-contribuir)
- [Configuración de desarrollo](#configuración-de-desarrollo)
- [Estándares de código](#estándares-de-código)
- [Proceso de pull request](#proceso-de-pull-request)
- [Reportar bugs](#reportar-bugs)
- [Sugerir funcionalidades](#sugerir-funcionalidades)
- [Vulnerabilidades de seguridad](#vulnerabilidades-de-seguridad)
- [Directrices de la comunidad](#directrices-de-la-comunidad)
- [Preguntas](#preguntas)

## Formas de contribuir

El código no es la única forma de ayudar:

- **Reportar bugs** — abre un issue con la plantilla de reporte de bug.
- **Sugerir funcionalidades** — describe el problema antes de proponer una solución.
- **Mejorar la documentación** — corrige erratas, ejemplos desactualizados o pasos confusos.
- **Clasificar issues** — reproduce reportes, añade detalles que falten o sugiere etiquetas.
- **Responder preguntas** — ayuda a otras personas en Discussions o en el issue tracker.

### Encontrar issues en los que trabajar

Busca las etiquetas `good first issue` o `help wanted` — los mantenedores las
curan para contribuidores nuevos. Comenta en un issue antes de empezar para
que nadie duplique tu trabajo.

## Configuración de desarrollo

    # 1. Haz fork del repositorio en GitHub y clona TU fork
    git clone https://github.com/[tu-usuario]/[repo].git
    cd [repo]

    # 2. Añade el repo original como upstream para sincronizar después
    git remote add upstream https://github.com/[org]/[repo].git

    # 3. Instala dependencias y verifica el entorno
    [comando de instalación]
    [comando de tests]

    # 4. Crea una rama para tu cambio
    git checkout -b feature/nombre-de-tu-feature

## Estándares de código

- Sigue las convenciones de estilo del lenguaje y framework en uso.
- Ejecuta el linter antes de hacer commit: `[comando de lint]`
- Formatea el código con: `[comando de formato]`
- Añade tests para cada funcionalidad nueva; mantén la cobertura por encima de [objetivo de cobertura]%.

### Mensajes de commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

    feat: añade validación de email al formulario de registro
    fix: resuelve null pointer en el reintento de pago
    docs: actualiza los ejemplos de la API para endpoints v2

Firma tus commits si el proyecto requiere una DCO (`git commit -s`). Revisa
`CLA.md` o `DCO.md` en el repositorio para conocer la política — algunos
proyectos aceptan contribuciones sin ningún acuerdo formal.

## Proceso de pull request

1. Crea la rama desde `main` con prefijo `feature/`, `fix/` o `docs/`.
2. Mantén el PR enfocado — un cambio por pull request.
3. Sube a tu fork y abre un PR con la plantilla provista.
4. Enlaza el issue relacionado: escribe `Closes #123` en la descripción.
5. Espera a que pase el CI y luego atiende el feedback de los revisores.
6. Un mantenedor hace merge cuando se aprueba. Haz squash si te lo piden.

### Checklist de PR

- [ ] Tests añadidos o actualizados
- [ ] Documentación actualizada
- [ ] El linter y el formatter pasan
- [ ] Los mensajes de commit siguen la convención
- [ ] La descripción del PR explica el qué y el por qué

## Reportar bugs

1. Busca primero entre los issues existentes — los duplicados se cierran.
2. Abre un issue nuevo con la plantilla de reporte de bug.
3. Incluye pasos para reproducir, comportamiento esperado frente al real,
   detalles del entorno (SO, versión) y logs o capturas cuando aplique.

## Sugerir funcionalidades

1. Abre un issue describiendo el problema que quieres resolver, no solo la
   API que quieres añadir.
2. Espera el feedback del mantenedor antes de escribir la implementación —
   las funcionalidades grandes pueden necesitar un RFC primero.
3. Una vez acordado, sigue el proceso de pull request de arriba.

## Vulnerabilidades de seguridad

**No abras un issue público para problemas de seguridad.** En su lugar:

- Reporta en privado a través de la política `SECURITY.md` o
  [contacto de seguridad / URL del advisory].
- Incluye una prueba de concepto o pasos de reproducción cuando sea posible.
- Espera una confirmación en un plazo de [tiempo de respuesta] días.

## Directrices de la comunidad

Este proyecto sigue el [Código de Conducta](CODE_OF_CONDUCT.md). Sé
respetuoso, asume buena intención y enfoca el feedback en el código — no en
la persona.

Los contribuidores aparecen como créditos en el README o en el archivo
`CONTRIBUTORS` y en las notas de release.

## Preguntas

- Abre una Discussion para preguntas generales.
- Únete a [URL de Discord/Slack] para chat en tiempo real.
- Escribe a [email de contacto] para consultas privadas.
