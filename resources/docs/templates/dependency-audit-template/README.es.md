# Plantilla de Auditoría de Dependencias de Terceros — Código complementario

Recursos complementarios para [Plantilla de Auditoría de Dependencias de Terceros](https://stackpractices.com/es/docs/dependency-audit-template/)
(EN: [Third-Party Dependency Audit Template](https://stackpractices.com/docs/dependency-audit-template/)).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `templates/dependency-audit-template.md` | El registro de auditoría listo para copiar: campos de resumen, checks de seguridad, umbrales de salud de mantenimiento, riesgo de supply chain y la fila de decisión de tres opciones |
| `automation/dependabot.yml` | Configuración de Dependabot con escaneos semanales y agrupación de patch/minor para que los PRs sigan siendo manejables |
| `scripts/license-check.sh` | Escanea el árbol de dependencias de producción y sale con error si una licencia copyleft (GPL/AGPL/LGPL/SSPL/…) se esconde en una dependencia transitiva |

## Uso

1. Copia `templates/dependency-audit-template.md` a `docs/audits/<libreria>.md` y rellena una por dependencia bajo revisión.
2. Obtén las cifras reales de [osv.dev](https://osv.dev), [deps.dev](https://deps.dev) y [OpenSSF Scorecard](https://scorecard.dev) — no rellenes umbrales de memoria.
3. Coloca `automation/dependabot.yml` en `.github/dependabot.yml` para que los CVEs nuevos abran PRs automáticamente.
4. Ejecuta `scripts/license-check.sh` en CI sobre el árbol de producción; una dependencia transitiva con GPL debería fallar el build, no aparecer en una due diligence.
5. Sigue el ciclo de vida pre-adopción → monitoreo → revisión trimestral → deprecación de la página principal.

## Licencia

MIT — ver la raíz del repositorio.
