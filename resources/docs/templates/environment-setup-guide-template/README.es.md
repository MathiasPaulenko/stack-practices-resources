# Plantilla de Guía de Configuración de Entorno — Recursos complementarios

Guía rellenable para documentar un setup de entorno reproducible: prerequisitos, inicio rápido, variables de entorno, verificación y troubleshooting.

## Archivos

- `environment-setup-guide-template.md` — plantilla de guía en blanco
- `Makefile` — automatización del setup con un comando (`make setup`)
- `devcontainer.json` — configuración de devcontainer para VS Code
- `.env.example` — plantilla de variables de entorno con valores ficticios
- `example-filled.md` — la guía rellenada para un proyecto ficticio

## Uso

Copia la plantilla en tu repositorio, ejecuta tu propio setup en una máquina limpia y transcribe cada comando. Actualiza la guía en la misma PR que cualquier cambio que afecte a los pasos de setup. Nunca subas secretos reales — usa `.env.example` con valores ficticios.

Fuente: https://stackpractices.com/es/docs/environment-setup-guide-template/
