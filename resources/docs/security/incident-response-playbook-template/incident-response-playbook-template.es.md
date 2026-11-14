# Playbook de Respuesta a Incidentes: `<Tipo de Incidente>`

## Metadatos del Incidente

| Campo | Valor |
|-------|-------|
| ID de Incidente | `INC-YYYY-MM-DD-###` |
| Severidad | `P1 (Crítico) / P2 (Alto) / P3 (Medio) / P4 (Bajo)` |
| Detectado Por | `@reporter` o `sistema_alerta` |
| Hora de Detección | `YYYY-MM-DD HH:MM UTC` |
| Líder de Respuesta | `@incident-commander` |
| Estado | `Abierto / Contenido / Erradicado / Cerrado` |

## 1. Detección

### 1.1. Validar la Alerta

- [ ] Confirmar que la alerta no es un falso positivo
- [ ] Recolectar evidencia inicial (logs, capturas de pantalla, capturas de red)
- [ ] Documentar el primer indicador de compromiso (IOC) observado

### 1.2. Clasificar Severidad

| Severidad | Criterios | Tiempo de Respuesta |
|----------|-----------|---------------------|
| P1 | Brecha de datos activa, ransomware, producción caída | < 15 minutos |
| P2 | Acceso admin no autorizado, malware detectado | < 1 hora |
| P3 | Intento de phishing, compromiso de cuenta de bajo privilegio | < 4 horas |
| P4 | Ruido de escaneo de vulnerabilidades, violación de política | < 24 horas |

### 1.3. Reunir al Equipo de Respuesta

- [ ] Asignar Incident Commander (único tomador de decisiones)
- [ ] Asignar Líder Técnico (forense y remediación)
- [ ] Asignar Líder de Comunicaciones (actualizaciones internas/externas)
- [ ] Avisar a los ingenieros de guardia de seguridad e infraestructura

## 2. Contención

### 2.1. Contención a Corto Plazo

- [ ] Aislar sistemas afectados (desconectar red, deshabilitar cuentas)
- [ ] Revocar credenciales comprometidas (API keys, contraseñas, tokens)
- [ ] Bloquear IPs maliciosas a nivel de firewall o WAF
- [ ] Preservar evidencia (snapshot de discos, exportar logs)

### 2.2. Contención a Largo Plazo

- [ ] Parchear la vulnerabilidad que habilitó el incidente
- [ ] Rotar todos los secretos en el alcance afectado
- [ ] Habilitar monitoreo adicional en sistemas relacionados
- [ ] Restringir el acceso a sistemas afectados solo al equipo de respuesta

## 3. Erradicación

- [ ] Eliminar malware, puertas traseras o cuentas no autorizadas
- [ ] Validar la integridad del sistema (checksums, baselines conocidos)
- [ ] Reconstruir sistemas comprometidos desde imágenes limpias
- [ ] Verificar que no quedan mecanismos de persistencia (cron jobs, tareas programadas)

## 4. Recuperación

- [ ] Restaurar sistemas desde backups limpios (verificar la integridad del backup primero)
- [ ] Rehabilitar servicios con monitoreo intensificado
- [ ] Validar funcionalidad con smoke tests
- [ ] Monitorear durante 24-72 horas por signos de reinfección
- [ ] Comunicar el visto bueno a los interesados

## 5. Lecciones Aprendidas

### 5.1. Línea de Tiempo

| Hora (UTC) | Acción | Responsable |
|------------|--------|-------------|
| `T+0` | Alerta disparada | `@system` |
| `T+15m` | Incident Commander asignado | `@security` |
| `T+45m` | Contención completa | `@infra` |
| `T+3h` | Erradicación completa | `@infra` |
| `T+6h` | Recuperación completa | `@app-team` |

### 5.2. Causa Raíz

- ¿Qué pasó?
- ¿Por qué fallaron nuestros controles?
- ¿Cuál fue el radio de impacto (usuarios, datos, sistemas)?

### 5.3. Acciones de Seguimiento

| ID | Acción | Responsable | Fecha Límite |
|----|--------|-------------|---------------|
| A1 | Agregar regla WAF para patrón de ataque | `@security` | +3 días |
| A2 | Habilitar MFA para todas las cuentas admin | `@identity` | +7 días |
| A3 | Mejorar retención de logs a 90 días | `@platform` | +14 días |
