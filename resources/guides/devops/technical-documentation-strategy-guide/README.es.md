# Estrategia de Documentación Técnica: Docs as Code — Plantillas

Recursos complementarios de la guía
[Estrategia de Documentación Técnica: Docs as Code](https://stackpractices.com/es/guides/technical-documentation-strategy-guide/).

## Contenido

| Fichero | Propósito |
|---------|-----------|
| `readme-template.md` | Esqueleto de README de servicio que responde las preguntas de un recién llegado, en orden. |
| `adr-template.md` | Plantilla de Architecture Decision Record: Estado, Contexto, Decisión, Consecuencias. |
| `runbook-template.md` | Plantilla de runbook indexado por síntomas: Síntomas → Diagnóstico → Resolución → Escalación. |
| `codeowners-example` | Ejemplo de `CODEOWNERS` que asigna ownership de docs por ruta. |
| `stale-docs-check.sh` | Script Bash que lista ficheros Markdown sin modificar en N días (365 por defecto). |

## Uso

Copia las plantillas en los repos de tus servicios y adáptalas:

```bash
cp readme-template.md /ruta/al/servicio/README.md
cp adr-template.md /ruta/al/servicio/adr/001-mi-decision.md
cp runbook-template.md /ruta/al/servicio/runbook.md
cp codeowners-example /ruta/al/servicio/.github/CODEOWNERS
```

Ejecuta el chequeo de docs obsoletos cada trimestre y asigna el resultado a los owners:

```bash
./stale-docs-check.sh 365 ./services
```

## Licencia

Ver el fichero `LICENSE` en la raíz del repositorio.
