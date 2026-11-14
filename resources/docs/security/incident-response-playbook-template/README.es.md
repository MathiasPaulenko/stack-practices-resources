# Plantilla de Playbook de Respuesta a Incidentes

Playbook rellenable en markdown para manejar incidentes de seguridad, estructurado en torno a las cinco fases de NIST SP 800-61: Detección, Contención, Erradicación, Recuperación y Lecciones Aprendidas.

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `incident-response-playbook-template.md` | Fillable playbook template (English) |
| `incident-response-playbook-template.es.md` | Plantilla rellenable del playbook (español) |

## Cómo usarla

1. Copia la plantilla una vez por tipo de incidente (brecha de datos, ransomware, DDoS, amenaza interna) — un playbook útil es específico, no genérico.
2. Reemplaza el placeholder `<Tipo de Incidente>` y adapta los checklists a tus herramientas (SIEM, firewall, proveedor de identidad).
3. Mantenla bajo control de versiones junto a tus runbooks y enlázala desde la documentación de guardias.
4. Corre un ejercicio de simulación trimestral y actualiza el playbook con lo aprendido.

La checklist también sirve como línea de tiempo del incidente: el escriba marca los ítems durante la respuesta, lo que se convierte en el registro para el postmortem.

## Fuente

Recurso complementario de [Plantilla de Playbook de Respuesta a Incidentes](https://stackpractices.com/es/docs/incident-response-playbook-template/) en StackPractices.com.
