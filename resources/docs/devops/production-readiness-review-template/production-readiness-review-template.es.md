# Production Readiness Review: `<Servicio / Feature>`

> Revisor: ______ | Fecha: ______ | Estado: Aprobado / Condicional / Rechazado
> Dueño del servicio: ______ | Equipo: ______ | Target de release: ______

---

## 1. Definición del Servicio

- [ ] El propósito del servicio está documentado y entendido por ingenieros de on-call
- [ ] El tier de servicio está definido (1 / 2 / 3) y coincide con requerimientos operacionales
- [ ] El documento de ownership de servicio está completo y accesible
- [ ] Las dependencias (upstream y downstream) están documentadas
- [ ] La clasificación de datos está definida (Público / Interno / Confidencial / Restringido)

## 2. Arquitectura y Calidad de Código

- [ ] La arquitectura fue revisada y aprobada por un ingeniero senior o arquitecto
- [ ] El código sigue estándares del equipo (linting, formato, cobertura de tests)
- [ ] No hay vulnerabilidades de seguridad conocidas en dependencias (escaneadas en 30 días)
- [ ] Los secretos se manejan vía secret manager, no hardcodeados ni en archivos de config
- [ ] No hay puntos únicos de falla sin mitigaciones documentadas

## 3. Testing

- [ ] La cobertura de unit tests está por encima del mínimo del equipo (usualmente 70-80%)
- [ ] Los integration tests cubren dependencias externas y caminos críticos
- [ ] Los load tests confirman que el servicio maneja el tráfico pico esperado
- [ ] Los chaos o failure injection tests verifican degradación controlada
- [ ] Los end-to-end tests cubren el recorrido completo del usuario donde aplica

## 4. Observabilidad

- [ ] Se emiten métricas para tasa de requests, errores y duración (RED)
- [ ] Los logs son estructurados, correlacionados con trace IDs y consultables
- [ ] El distributed tracing está configurado para requests entre servicios
- [ ] Existen dashboards para salud del servicio y métricas clave de negocio
- [ ] Las reglas de alertado están configuradas con severidad y umbrales apropiados
- [ ] Los ingenieros de on-call pueden distinguir entre síntomas y causas

## 5. Confiabilidad y Resiliencia

- [ ] Existe endpoint de health check y es usado por load balancers
- [ ] Circuit breakers o bulkheads protegen contra fallas en cascada
- [ ] Timeouts y retries están configurados para llamadas externas
- [ ] Rate limiting está en marcha para endpoints públicos o de socios
- [ ] Las conexiones a base de datos están pooleadas y acotadas
- [ ] El servicio degrada de forma controlada cuando dependencias fallan

## 6. Despliegue y Release

- [ ] Existe pipeline CI/CD y está verde
- [ ] Los deploys son automatizados; no se requieren cambios manuales en producción
- [ ] Canary o staged rollout está configurado para servicios de alto tier
- [ ] Feature flags están disponibles para cambios riesgosos o irreversibles
- [ ] Las migraciones de base de datos son compatibles hacia atrás o tienen rollback probado
- [ ] El procedimiento de rollback está documentado y probado en los últimos 30 días

## 7. Seguridad

- [ ] Autenticación y autorización están implementadas correctamente
- [ ] Validación y sanitización de inputs protegen contra ataques de inyección
- [ ] Encriptación en tránsito (TLS 1.2+) está forzada
- [ ] Datos sensibles están encriptados en reposo
- [ ] Revisión de seguridad completada para cambios de auth, pagos o manejo de datos
- [ ] Resultados de pentest o security scan revisados y remediados

## 8. Datos y Estado

- [ ] Cambios de esquema de base de datos fueron revisados por impacto en rendimiento
- [ ] Backups están configurados y probados (restore verificado en 90 días)
- [ ] Políticas de retención de datos están documentadas y aplicadas
- [ ] Requerimientos GDPR / CCPA / compliance se cumplen para datos de usuarios
- [ ] Scripts de migración son idempotentes y reversibles donde sea posible

## 9. Documentación

- [ ] El README explica cómo construir, testear y ejecutar el servicio localmente
- [ ] La documentación de API está actualizada (OpenAPI / Swagger / equivalente)
- [ ] Existen runbooks para: deploy, rollback, incidentes comunes y escalamiento
- [ ] El documento de handoff de on-call está actualizado con cambios y riesgos recientes
- [ ] Los ADRs cubren decisiones de diseño mayores

## 10. Preparación Operacional

- [ ] La rotación de on-call está cubierta y entrenada en este servicio
- [ ] Las alertas de paging llegan a las personas correctas con contexto útil
- [ ] La ruta de escalamiento está documentada y los contactos verificados
- [ ] Los runbooks fueron probados por alguien que no escribió el servicio
- [ ] Los pasos de verificación post-deploy están definidos y automatizados donde sea posible

---

## Notas de Revisión

| Item | Hallazgo | Riesgo | Mitigación / Acción | Responsable | Fecha límite |
|------|----------|--------|---------------------|-------------|--------------|
| ______ | ______ | Alto / Medio / Bajo | ______ | ______ | ______ |

## Sign-Off

| Rol | Nombre | Fecha | Firma (aprobar / bloquear) |
|-----|--------|-------|---------------------------|
| Dueño de ingeniería | ______ | ______ | ______ |
| Product owner | ______ | ______ | ______ |
| Revisor de seguridad | ______ | ______ | ______ |
| SRE / Plataforma | ______ | ______ | ______ |
