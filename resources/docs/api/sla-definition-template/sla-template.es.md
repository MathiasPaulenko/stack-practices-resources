# Acuerdo de Nivel de Servicio: `<Nombre del Servicio>`

**Fecha de Efectividad:** `2026-07-01`
**Ciclo de Revisión:** `Trimestral`
**Equipo Responsable:** `@equipo-plataforma`
**Medido por:** `Prometheus + dashboard compartido de Grafana`

## 1. Objetivos de Nivel de Servicio (SLOs)

| Métrica | Objetivo | Ventana de Medición | Fuente de Datos |
|---------|----------|---------------------|-----------------|
| Disponibilidad | 99.9% | 30 días rodante | Health checks del LB |
| Latencia p95 | < 200ms | Por minuto | Métricas de app (Prometheus) |
| Latencia p99 | < 500ms | Por minuto | Métricas de app (Prometheus) |
| Tasa de Error | < 0.1% | 7 días rodante | Logs de app + APM |
| Throughput | > 1,000 req/s | Por minuto | Métricas del LB |

## 2. Indicadores de Nivel de Servicio (SLIs)

| SLI | Eventos Buenos | Eventos Válidos | Cálculo |
|-----|----------------|-----------------|---------|
| Disponibilidad | Checks exitosos | Todos los checks | Buenos / Válidos |
| Latencia p95 | Solicitudes < 200ms | Todas las solicitudes | Percentil de válidos |
| Tasa de Error | Respuestas < 500 | Todas las respuestas | 1 - (errores / total) |

## 3. Presupuesto de Error

| SLO | Presupuesto (30 días) | Alerta de Burn |
|-----|------------------------|----------------|
| 99.9% disponibilidad | 43.2 min caída | 2x en 1 día = warn |
| < 0.1% tasa de error | 0.1% de solicitudes | 10x en 1 día = freeze |

### Alertas de Burn Rate

| Burn Rate | Presupuesto Consumido | Acción |
|-----------|-----------------------|--------|
| 1x | Al ritmo esperado | Monitorear |
| 2x | 2x más rápido | Avisar a guardia |
| 10x | 10x más rápido | Avisar + congelar deploys |

## 4. Tiempos de Respuesta y Resolución

| Severidad | Definición | Respuesta | Resolución | Escalamiento |
|-----------|------------|-----------|------------|--------------|
| P1 | Caída total | 15 min | 2 horas | VP Ingeniería |
| P2 | Degradado, workaround | 1 hora | 8 horas | Eng. Manager |
| P3 | Fallo parcial | 4 horas | 3 días hábiles | Team Lead |
| P4 | Cosmético | 1 día hábil | Próximo sprint | Cola de tickets |

## 5. Exclusiones

Lo siguiente queda excluido del cálculo del SLA:
- **Mantenimiento programado:** <=4 horas/mes con 7 días de aviso
- **Caídas de terceros:** Dependencias fuera de nuestro control
- **Fuerza mayor:** Desastres, fallos de backbone
- **Problemas del cliente:** Bugs del consumidor, abuso de rate limit

## 6. Penalizaciones y Créditos

| Uptime Mensual | Crédito de Servicio | Disparador |
|----------------|---------------------|------------|
| 99.0% - 99.9% | 10% de la cuota | Automático |
| 95.0% - 99.0% | 25% de la cuota | Automático |
| < 95.0% | 50% de la cuota | Auto + postmortem |

## 7. Plan de Comunicación

| Evento | Audiencia | Canal | Momento |
|--------|-----------|-------|---------|
| Degradación detectada | Interno | PagerDuty + Slack | Inmediato |
| Inicio de caída P1 | Clientes | Status page + email | <=30 min |
| P1 resuelta | Clientes | Status page | <=15 min después |
| Reporte mensual SLA | Clientes | Email | <=5 días hábiles |

## 8. Revisión y Actualización

- **Revisión trimestral:** Ingeniería + Producto + Customer Success
- **Revisión por evento:** Toda P1 o incumplimiento dispara revisión
- **Aviso de cambios:** 14 días antes de que entren en vigor
