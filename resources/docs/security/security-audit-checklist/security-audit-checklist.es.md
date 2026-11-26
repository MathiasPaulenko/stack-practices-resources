# Checklist de Auditoría de Seguridad

Alcance: `<Nombre del sistema/organización>` | Auditor: `<Nombre>` | Fecha: `<AAAA-MM-DD>`

## 1. Seguridad de Red

- [ ] Reglas de firewall documentadas y en control de versiones
- [ ] Política de denegación por defecto; sin reglas any-any
- [ ] Reglas revisadas trimestralmente; sin reglas sin uso
- [ ] Acceso de gestión restringido (solo VPN / jump host)
- [ ] DMZ configurada; redes de producción y BD aisladas
- [ ] NetworkPolicies de Kubernetes (denegación entre namespaces)
- [ ] DNSSEC en zonas públicas; filtrado y logging DNS
- [ ] Mitigación DDoS en el borde; limitación de tasa en APIs

## 2. Seguridad de Aplicaciones

- [ ] MFA obligatorio para todos los usuarios (TOTP o llave hardware)
- [ ] Contraseñas con Argon2id/bcrypt; verificación de filtradas
- [ ] Sesiones: expiración por inactividad y absoluta, cookies Secure
- [ ] RBAC aplicado en servidor; mínimo privilegio
- [ ] Revisiones de acceso trimestrales; JIT para acceso privilegiado
- [ ] Consultas parametrizadas en todo (nada de SQL por concatenación)
- [ ] Codificación de salida + CSP contra XSS
- [ ] Cookies SameSite + tokens CSRF en cambios de estado
- [ ] Validación de subidas (tipo, tamaño, antivirus)
- [ ] Lista permitida contra SSRF en peticiones salientes
- [ ] Cabeceras: CSP, HSTS, X-Content-Type-Options, X-Frame-Options
- [ ] Escaneo de dependencias en CI; umbral 0 críticas/altas
- [ ] SBOM por release; imágenes de contenedor escaneadas

## 3. Protección de Datos

- [ ] TLS 1.2+ en todo; SSLv3 / TLS 1.0/1.1 deshabilitados
- [ ] Certificados con renovación automática y alerta de expiración
- [ ] Cifrado en reposo: bases de datos, object storage, volúmenes
- [ ] Cifrado a nivel de campo para PII
- [ ] Clasificación aplicada; PII identificada y etiquetada
- [ ] Retención aplicada automáticamente; borrado seguro
- [ ] Backups cifrados; restauración probada mensualmente
- [ ] Sin secretos en código, logs ni archivos .env
- [ ] Secretos en vault; rotación automática; accesos registrados

## 4. Seguridad de Infraestructura

- [ ] Benchmarks CIS aplicados; deriva monitorizada
- [ ] Sin buckets ni bases de datos públicas; solo subredes privadas
- [ ] IAM de mínimo privilegio; sin wildcards en producción
- [ ] CloudTrail / logs de auditoría en todas las regiones con integridad
- [ ] Pod Security Standards (Restricted); sin contenedores privilegiados/root
- [ ] readOnlyRootFilesystem; admission controllers (Kyverno/OPA)
- [ ] Baseline del SO endurecido; servicios innecesarios deshabilitados
- [ ] SSH solo con clave; PermitRootLogin no; fail2ban
- [ ] Actualizaciones de seguridad automáticas; FIM; IDS en el host

## 5. Monitorización y Logging

- [ ] Todas las fuentes de logs llegan al SIEM (app, acceso, auditoría, firewall, cloud)
- [ ] Retención por tipo de log (auditoría >= 1 año)
- [ ] Alertas de fuerza bruta, escalada de privilegios, exfiltración, malware
- [ ] Falsos positivos < 5%; fatiga de alertas monitorizada
- [ ] Feed de inteligencia de amenazas integrado; incidentes cerrados

## 6. Respuesta a Incidentes

- [ ] Plan de IR documentado y actualizado
- [ ] Equipo de IR definido con guardia 24/7
- [ ] Escalado por severidad; contactos actualizados mensualmente
- [ ] Ejercicio tabletop en los últimos 6 meses
- [ ] Revisiones post-incidente (sin culpables) en cada incidente
- [ ] MTTD / MTTR medidos contra objetivos

## 7. Cumplimiento

- [ ] Controles SOC 2 mapeados a evidencia (CC6.x, CC7.x, CC8.1)
- [ ] ROPA actualizado; gestión de consentimiento; SLA de DSR cumplido
- [ ] Procedimiento de notificación de brechas en 72 h probado
- [ ] Controles del Anexo A de ISO 27001 revisados anualmente
- [ ] Proveedores con acceso a datos con DPA/BAA firmados
- [ ] Pentest externo en los últimos 12 meses

## Hallazgos

| # | Hallazgo | Severidad | Evidencia | Responsable | Fecha límite |
|---|----------|-----------|-----------|-------------|--------------|
| 1 | | | | | |
