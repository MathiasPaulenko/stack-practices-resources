# Plantilla de Reporte de Bug — Recursos complementarios

Archivos complementarios de la [Plantilla de Reporte de Bug](https://stackpractices.com/es/docs/bug-report-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `bug-report-template.md` | Markdown | Plantilla de reporte de bug lista para copiar con niveles de severidad y campos de evidencia |
| `github-issue-form.yml` | YAML | Formulario de issue de GitHub que exige pasos de reproducción y severidad como campos obligatorios |
| `gitlab-issue-template.md` | Markdown | Plantilla de descripción de issue de GitLab — se coloca en `.gitlab/issue_templates/` |

## Inicio rápido

### 1. Copia la plantilla Markdown

```bash
cp bug-report-template.md BUG-1234-export-vacio.md
```

Edita la copia y reemplaza cada placeholder (`'...'`, `[e.g., ...]`) con valores reales.

### 2. Instala el formulario de issue de GitHub

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp github-issue-form.yml .github/ISSUE_TEMPLATE/bug-report.yml
```

Haz commit y push — quienes reporten verán un formulario estructurado en lugar de un cuadro de texto vacío, y `validations.required` bloquea el envío sin pasos de reproducción.

### 3. Alternativa en GitLab

```bash
mkdir -p .gitlab/issue_templates
cp gitlab-issue-template.md .gitlab/issue_templates/Bug.md
```

GitLab prellena la descripción desde la plantilla cuando alguien la elige en el formulario de nuevo issue. Los campos se exigen por convención — la plantilla incluye las mismas secciones más los quick actions `/label ~bug ~triage` al final.

## Estructura de la plantilla

1. **Resumen** — qué falla, dónde, bajo qué condición
2. **Pasos para Reproducir** — numerados, desde un estado conocido
3. **Comportamiento Esperado vs Actual** — define qué significa "corregido"
4. **Entorno** — SO, navegador, versión de la app, ambiente de despliegue
5. **Introducido En** — primera versión donde aparece el bug
6. **Severidad** — Crítica / Alta / Media / Baja
7. **Evidencia** — capturas, logs, IDs de request
8. **Contexto Adicional** — frecuencia, trabajo relacionado, cambios recientes
