# Runbook de Respuesta a Incidentes de LLM — Recursos complementarios

Archivos complementarios del [Runbook de Respuesta a Incidentes de LLM](https://stackpractices.com/es/docs/ai-llm-incident-response-runbook/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `llm-incident-runbook.md` | Markdown | Runbook independiente: niveles de severidad, ruta de escalado, tabla de contactos, cinco playbooks de incidentes, checklist post-incidente |
| `check-llm-status.sh` | Bash | Verificación de salud de proveedores: consulta páginas de estado y prueba conectividad de API; sale con código distinto de cero si hay caída |

## Inicio rápido

### 1. Copia el runbook

```bash
cp llm-incident-runbook.md oncall/runbooks/llm-incident-response.md
```

Completa cada `[placeholder]`: contactos, canales, servicio de guardia y tus umbrales de severidad.

### 2. Ejecuta la verificación de estado

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

./check-llm-status.sh
```

Cada línea reporta `OK`, `FAIL` o `SKIP` (cuando la variable de entorno de la API key no está definida). El código de salida es distinto de cero si alguna comprobación falla — conéctalo a tu alertado o ejecútalo primero cuando aplique la sección 3 del runbook.

## Adáptalo antes de producción

1. Ajusta la tabla de severidad a tu tráfico y margen de presupuesto.
2. Lista qué funcionalidades de IA puedes desactivar — decídelo ahora, no durante la caída.
3. Verifica que cada contacto llega efectivamente a una persona.
