# Plan de Respuesta a Incidentes — `<Nombre de la Organización>`

## Resumen del Plan

| Campo | Valor |
|-------|-------|
| Organización | Example Corp |
| Versión del plan | 3.0 |
| Última actualización | 2026-07-05 |
| Responsable del plan | CISO |
| Aprobado por | Comité Ejecutivo |
| Ciclo de revisión | Trimestral |
| Próxima revisión | 2026-10-05 |
| Marcos de cumplimiento | SOC 2, ISO 27001, GDPR, HIPAA |
| Tamaño del equipo IR | 7 miembros |
| Rotación de guardia | 24/7, rotación semanal |

## 1. Clasificación de Severidad del Incidente

### Niveles de Severidad

| Severidad | Definición | Ejemplos | Tiempo de respuesta | Escalamiento |
|-----------|------------|----------|---------------------|--------------|
| SEV-0 (Crítica) | Caída total del servicio o fuga de datos activa | Producción caída, PII filtrada, ransomware | 15 min | CEO, CISO, Legal, PR |
| SEV-1 (Alta) | Degradación mayor del servicio o brecha confirmada | Caída parcial, acceso no autorizado detectado | 30 min | CISO, VP Engineering |
| SEV-2 (Media) | Degradación menor o problema de seguridad sospechado | Respuesta lenta, actividad sospechosa marcada | 2 horas | Security Lead, Ing. de guardia |
| SEV-3 (Baja) | Problema menor sin impacto en usuarios | Caída de un pod, error de configuración | 4 horas | Ingeniero de guardia |
| SEV-4 (Informativa) | Sin impacto, solo informativo | Aviso de seguridad, notificación de mantenimiento | Siguiente día laborable | N/A |

### Matriz de Decisión de Severidad

| Impacto \ Alcance | Un usuario | Equipo | Departamento | Organización |
|-------------------|------------|--------|--------------|--------------|
| Fuga de datos | SEV-1 | SEV-0 | SEV-0 | SEV-0 |
| Caída del servicio | SEV-3 | SEV-2 | SEV-1 | SEV-0 |
| Degradación de rendimiento | SEV-4 | SEV-3 | SEV-2 | SEV-1 |
| Alerta de seguridad (sin confirmar) | SEV-3 | SEV-2 | SEV-2 | SEV-1 |

## 2. Roles y Responsabilidades

### Equipo de Respuesta a Incidentes

| Rol | Titular | Suplente | Responsabilidades |
|-----|---------|----------|-------------------|
| Comandante de Incidente (IC) | CISO | VP Engineering | Coordinar la respuesta, decidir, autorizar acciones |
| Líder Técnico | Security Lead | Senior DevOps | Investigar, contener, erradicar la amenaza |
| Líder de Comunicación | Director de PR | Director de Marketing | Comunicaciones internas y externas |
| Asesor Legal | General Counsel | Legal Externo | Obligaciones legales, notificaciones regulatorias |
| Enlace de RR. HH. | Director de RR. HH. | Gerente de RR. HH. | Temas de personal, investigaciones internas |
| Escribano | Security Analyst | Ingeniero DevOps | Documentar cronología, decisiones, acciones |
| Patrocinador Ejecutivo | CEO | COO | Decisiones de negocio, autorización de recursos |

### Calendario de Guardias

| Rotación | Guardia titular | Guardia suplente | Escalamiento |
|----------|-----------------|------------------|--------------|
| Semana 1 | Security Lead A | Ingeniero DevOps A | CISO |
| Semana 2 | Security Lead B | Ingeniero DevOps B | CISO |
| Semana 3 | Security Lead A | Ingeniero DevOps A | VP Eng |
| Semana 4 | Security Lead B | Ingeniero DevOps B | VP Eng |
| Festivos | Security Lead C | Ingeniero DevOps C | CISO + VP Eng |

### Información de Contacto

| Rol | Nombre | Teléfono | Email | Slack |
|-----|--------|----------|-------|-------|
| Comandante de Incidente | Jane Doe | +1-555-0101 | jane@example.com | @jane |
| Líder Técnico | John Smith | +1-555-0102 | john@example.com | @john |
| Líder de Comunicación | Mary Johnson | +1-555-0103 | mary@example.com | @mary |
| Asesor Legal | Robert Chen | +1-555-0104 | robert@example.com | @robert |
| Enlace de RR. HH. | Sarah Williams | +1-555-0105 | sarah@example.com | @sarah |
| Patrocinador Ejecutivo | CEO | +1-555-0100 | ceo@example.com | @ceo |

## 3. Ciclo de Vida del Incidente

### Fase 1: Detección y Reporte

| Fuente de detección | Método | Destino de la alerta | Respuesta |
|---------------------|--------|----------------------|-----------|
| Alertas SIEM | Reglas de correlación | Seguridad de guardia | Avisar al de guardia |
| Alertas de monitoreo | Datadog/Prometheus | DevOps de guardia | Avisar al de guardia |
| Reportes de usuarios | Ticket de help desk | Equipo de seguridad | Triaje en 1 hora |
| Reportes externos | Investigador de seguridad | Security Lead | Acusar recibo en 24 horas |
| Inteligencia de amenazas | Correlación de feeds | Alerta automática SIEM | Aviso automático en SEV-0/1 |
| Cumplimiento | Hallazgo de auditoría | Security Lead | Triaje en 1 día laborable |

### Plantilla de Reporte de Incidente

```
ID del incidente: INC-2026-001
Reportado por: <nombre>
Fecha/hora de detección: <AAAA-MM-DD HH:MM TZ>
Severidad: <SEV-0/1/2/3/4>
Descripción: <descripción breve>
Sistemas afectados: <lista>
Usuarios afectados: <cantidad o "desconocido">
Datos involucrados: <tipo, clasificación>
Estado actual: <investigando/contenido/resuelto>
Asignado a: <nombre>
```

### Fase 2: Triaje y Evaluación

| Paso | Acción | Responsable | Duración |
|------|--------|-------------|----------|
| 1 | Acusar recibo del incidente | Guardia | 5 min |
| 2 | Asignar ID de incidente | Guardia | 5 min |
| 3 | Evaluar severidad | Guardia + IC | 15 min |
| 4 | Asignar roles | IC | 10 min |
| 5 | Crear canal del incidente | Escribano | 5 min |
| 6 | Notificar a interesados | Líder de Comunicación | 30 min |
| 7 | Iniciar registro del incidente | Escribano | Continuo |
| 8 | Comenzar investigación | Líder Técnico | Continuo |

### Fase 3: Contención

#### Contención inmediata (SEV-0/SEV-1)

| Acción | Comando/Procedimiento | Duración | Aprobación |
|--------|-----------------------|----------|------------|
| Aislar el host afectado | `kubectl cordon <node>; kubectl drain <node>` | 5 min | Líder Técnico |
| Bloquear IP maliciosa | Actualizar reglas WAF / firewall | 5 min | Líder Técnico |
| Deshabilitar cuenta comprometida | `aws iam update-access-key --status Inactive` | 5 min | Líder Técnico |
| Revocar sesiones activas | Cierre de sesión forzado vía IdP | 5 min | Líder Técnico |
| Deshabilitar servicio afectado | `kubectl scale deployment <name> --replicas=0` | 5 min | IC |
| Capturar imágenes de disco | Crear snapshots para forense | 15 min | Líder Técnico |
| Preservar evidencia | Capturar logs, volcados de memoria | 30 min | Líder Técnico |

#### Contención a corto plazo

| Acción | Propósito | Duración |
|--------|-----------|----------|
| Aplicar reglas temporales de firewall | Bloquear el vector de ataque | 30 min |
| Rotar credenciales comprometidas | Evitar reingreso | 1 hora |
| Parchear software vulnerable | Cerrar el vector de ataque | 2-4 horas |
| Desplegar hotfix | Corregir el bug explotado | 2-6 horas |

#### Contención a largo plazo

| Acción | Propósito | Duración |
|--------|-----------|----------|
| Reconstruir sistemas afectados | Estado limpio | 4-24 horas |
| Actualizar reglas de seguridad | Prevenir recurrencia | 1-2 horas |
| Reforzar el monitoreo | Detectar ataques similares | 2-4 horas |
| Actualizar reglas de detección | Correlación SIEM | 1-2 horas |

### Fase 4: Erradicación

| Paso | Acción | Verificación |
|------|--------|--------------|
| 1 | Identificar la causa raíz | Análisis forense |
| 2 | Eliminar malware/artefactos | Escaneo anti-malware, revisión manual |
| 3 | Cerrar el vector de ataque | Parche, cambio de configuración, regla |
| 4 | Validar la erradicación | Escaneo completo, prueba de penetración |
| 5 | Documentar los pasos | Registro del incidente actualizado |

### Fase 5: Recuperación

| Paso | Acción | Verificación | Duración |
|------|--------|--------------|----------|
| 1 | Restaurar desde backup limpio | Verificar integridad del backup | 1-4 horas |
| 2 | Reconstruir sistemas afectados | Validación de configuración | 2-12 horas |
| 3 | Desplegar versión parcheada | Smoke tests correctos | 1-2 horas |
| 4 | Restaurar tráfico gradualmente | Health checks, monitoreo | 30 min - 2 horas |
| 5 | Vigilar recurrencia | Monitoreo reforzado 72 horas | 72 horas |
| 6 | Validar con usuarios | Pruebas de aceptación | 1-4 horas |

### Fase 6: Revisión Post-Incidente

| Paso | Acción | Responsable | Duración |
|------|--------|-------------|----------|
| 1 | Programar la reunión de revisión | IC | Dentro de 5 días |
| 2 | Recopilar toda la evidencia | Escribano | Antes de la reunión |
| 3 | Redactar la cronología del incidente | Escribano | Antes de la reunión |
| 4 | Realizar revisión sin culpables | Todos los interesados | 1-2 horas |
| 5 | Identificar la causa raíz | Líder Técnico | Durante la revisión |
| 6 | Definir acciones correctivas | Equipo | Durante la revisión |
| 7 | Asignar acciones con responsables | IC | Durante la revisión |
| 8 | Publicar el post-mortem | Escribano | Dentro de 2 semanas |
| 9 | Dar seguimiento a las acciones | IC | Hasta completarlas |

## 4. Plan de Comunicación

### Comunicaciones Internas

| Audiencia | Canal | Frecuencia | Contenido |
|-----------|-------|------------|-----------|
| Equipo IR | Canal de Slack del incidente | Tiempo real | Actualizaciones técnicas |
| Ingeniería | Slack #incidents | Cada 30 min | Actualizaciones de estado |
| Toda la plantilla | Email | Cada 2 horas | Estado de alto nivel |
| Equipo ejecutivo | Teléfono/Slack | Cada hora | Impacto en el negocio |
| Junta directiva | Email vía CEO | Dentro de 24 horas | Resumen para la junta |

### Comunicaciones Externas

| Audiencia | Canal | Frecuencia | Contenido | Aprobación |
|-----------|-------|------------|-----------|------------|
| Clientes | Página de estado | Dentro de 30 min | Impacto en el servicio | IC + Comms |
| Clientes | Email | Dentro de 24 horas | Notificación detallada | IC + Legal |
| Autoridades reguladoras | Notificación oficial | Según regulación | Divulgación requerida | Legal |
| Medios | Comunicado de prensa | Si es público | Declaración aprobada | CEO + Comms |
| Investigadores de seguridad | Email | Dentro de 48 horas | Acuse de recibo | Security Lead |

### Plantillas de Comunicación

#### Actualización de página de estado (inicial)

```
[INVESTIGANDO] Estamos investigando un problema que afecta a <servicio>.
Impacto: <descripción del impacto>.
Inicio: <marca de tiempo>.
Publicaremos una actualización en 30 minutos.
```

#### Actualización de página de estado (resuelto)

```
[RESUELTO] El problema que afectaba a <servicio> se ha resuelto.
Duración: de <inicio> a <fin>.
Causa raíz: <descripción breve>.
Publicaremos una revisión post-incidente en 2 semanas.
```

#### Email de notificación a clientes

```
Asunto: Notificación de incidente de seguridad — <Fecha>

Estimado/a <Cliente>:

Le escribimos para informarle de un incidente de seguridad que puede
haber afectado a sus datos.
<Descripción del incidente y su impacto>.
<Qué hemos hecho en respuesta>.
<Qué deben hacer los clientes>.
Nos lo tomamos en serio y estamos tomando estas medidas: <lista de acciones>.
Para cualquier duda, escríbanos a security@example.com.

Atentamente,
<Nombre>, <Cargo>
```

## 5. Requisitos de Notificación Regulatoria

| Regulación | Plazo de notificación | Destinatario | Disparador |
|------------|-----------------------|--------------|------------|
| GDPR | 72 horas | Autoridad de control | Brecha de datos personales |
| GDPR | Sin demora indebida | Interesados | Alto riesgo para sus derechos |
| CCPA | Sin demora injustificada | Consumidores afectados | Brecha de PII |
| HIPAA | 60 días | Secretario del HHS | Brecha de PHI de 500+ personas |
| HIPAA | 60 días | Personas afectadas | Brecha de PHI |
| SOC 2 | Según acuerdo | Clientes | Incidente de seguridad |
| Leyes estatales | Variable (1-90 días) | Fiscal estatal + residentes | Según ley estatal |

## 6. Métricas del Incidente

| Métrica | Objetivo | Medición | Reporte |
|---------|----------|----------|---------|
| Tiempo medio de detección (MTTD) | < 15 min | Del inicio del incidente a la detección | Mensual |
| Tiempo medio de respuesta (MTTR) | < 30 min | De la detección al inicio de la respuesta | Mensual |
| Tiempo medio de contención (MTTC) | < 4 horas | De la detección a la contención | Mensual |
| Tiempo medio de recuperación (MTTR) | < 24 horas | De la contención a la recuperación total | Mensual |
| Incidentes por trimestre | Tendencia a la baja | Recuento de incidentes | Trimestral |
| Incidentes repetidos | < 5% | Incidentes con la misma causa raíz | Trimestral |
| Revisiones post-incidente a tiempo | 100% | Revisiones dentro de 5 días | Mensual |
| Acciones correctivas completadas | 100% | Acciones ejecutadas | Trimestral |
| Ejercicios de simulación | 4 por año | Ejercicios realizados | Anual |

## 7. Plan de Ejercicios de Simulación

### Calendario de Ejercicios

| Ejercicio | Escenario | Participantes | Frecuencia |
|-----------|-----------|---------------|------------|
| Ejercicio 1 | Ataque de ransomware | Equipo IR completo | Trimestral |
| Ejercicio 2 | Fuga de datos (PII) | Equipo IR + Legal + PR | Trimestral |
| Ejercicio 3 | Amenaza interna | Equipo IR + RR. HH. | Anual |
| Ejercicio 4 | Ataque DDoS | Equipo IR + DevOps | Anual |
| Ejercicio 5 | Ataque a la cadena de suministro | Equipo IR + Ejecutivos | Anual |

### Formato del Ejercicio

| Fase | Duración | Actividad |
|------|----------|-----------|
| Preparación | 15 min | Repartir el escenario, asignar roles |
| Inyecto 1 | 30 min | Reporte inicial del incidente |
| Inyecto 2 | 30 min | Escalamiento (nueva información) |
| Inyecto 3 | 30 min | Complicación (persona clave no disponible) |
| Hot wash | 30 min | Retroalimentación inmediata y lecciones |
| Informe | 1 semana | Hallazgos y recomendaciones por escrito |
