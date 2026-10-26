# Política de Control de Acceso — `<Nombre de la Organización>`

## Resumen de la Política

| Campo | Valor |
|-------|-------|
| Organización | Example Corp |
| Versión de la política | 2.0 |
| Última actualización | 2026-10-24 |
| Responsable | CISO |
| Aprobada por | Comité Ejecutivo |
| Ciclo de revisión | Anual |
| Próxima revisión | 2027-10-24 |
| Frameworks de compliance | SOC 2, ISO 27001, HIPAA |
| Modelo de acceso | RBAC + ABAC (híbrido) |

## 1. Autenticación

### Métodos de Autenticación

| Método | Caso de uso | MFA requerido | Notas |
|--------|-------------|---------------|-------|
| Contraseña + MFA | Login de usuario (todos) | Sí (TOTP o llave hardware) | Por defecto para todos los usuarios |
| SSO (SAML/OIDC) | Apps empresariales | Sí (vía IdP) | Okta como IdP |
| API keys | Servicio a servicio | N/A | Rotación cada 90 días |
| OAuth 2.0 | Integraciones de terceros | N/A | Tokens con scope, caducidad de 1 hora |
| Claves SSH | Acceso a servidores | Sí (MFA en jump host) | Solo claves Ed25519 |
| Certificados de cliente | Servicios mTLS | N/A | Emitidos por la CA interna |

### Política de Contraseñas

| Requisito | Valor | Justificación |
|-----------|-------|---------------|
| Longitud mínima | 14 caracteres | Resistencia a fuerza bruta |
| Clases de caracteres | 3 de 4 (mayús., minús., dígito, especial) | Complejidad sin reglas de complejidad |
| Historial | Últimas 24 contraseñas | Prevenir reutilización |
| Caducidad | Sin máximo (guía NIST) | Los cambios frecuentes debilitan las contraseñas |
| Check de filtraciones | Verificar contra Have I Been Pwned | Prevenir uso de contraseñas filtradas |
| Umbral de bloqueo | 10 intentos fallidos | Cuenta bloqueada tras 10 intentos |
| Duración del bloqueo | 15 minutos | Desbloqueo automático a los 15 min |
| Almacenamiento | Hash Argon2id | Memory-hard, dificulta el cracking |

### Autenticación Multifactor (MFA)

| Grupo de usuarios | Método MFA | Aplicación | Recuperación |
|-------------------|------------|------------|--------------|
| Todos los empleados | TOTP (Google Authenticator) | Obligatorio al login | Códigos de respaldo |
| Administradores | Llave hardware (YubiKey) | Obligatorio al login | Llave hardware de respaldo |
| Desarrolladores | TOTP o llave hardware | Obligatorio para acceso a prod | Códigos de respaldo |
| Cuentas de servicio | Sin MFA (API key) | N/A | Rotación de claves |
| Contratistas | TOTP | Obligatorio al login | Gestionado por el sponsor |

### Proceso de Alta en MFA

| Paso | Acción | Responsable | Duración |
|------|--------|-------------|----------|
| 1 | El usuario solicita el alta en MFA | Usuario | — |
| 2 | IT verifica la identidad | Soporte IT | 1 día hábil |
| 3 | El usuario instala la app autenticadora | Usuario | 15 minutos |
| 4 | El usuario escanea el código QR | Usuario + IT | 5 minutos |
| 5 | El usuario verifica con un código de prueba | Usuario | 2 minutos |
| 6 | El usuario guarda los códigos de respaldo | Usuario | 5 minutos |
| 7 | IT activa la obligatoriedad de MFA | Soporte IT | Mismo día |

## 2. Autorización

### Control de Acceso Basado en Roles (RBAC)

| Rol | Descripción | Permisos | Asignación |
|-----|-------------|----------|------------|
| Viewer | Acceso de solo lectura | Ver dashboards, informes | Asignado automáticamente a todos los empleados |
| Developer | Acceso de desarrollo | Repos de código, CI/CD, staging | Aprobación del manager |
| Senior Developer | Desarrollo + revisión | Repos, CI/CD, staging, lectura de prod | Aprobación de manager + tech lead |
| DevOps Engineer | Acceso a infraestructura | Toda la infra, deploy a prod | Aprobación de manager + CISO |
| Administrator | Acceso completo | Todos los sistemas, gestión de usuarios | Aprobación de manager + CISO + CEO |
| Auditor | Acceso de lectura para auditoría | Logs de acceso, informes de auditoría | Aprobación del CISO |
| Service Account | Acceso automatizado | Endpoints de API específicos | Aprobación del responsable técnico |

### Matriz de Permisos

| Recurso | Viewer | Developer | Senior Dev | DevOps | Admin | Auditor |
|---------|--------|-----------|------------|--------|-------|---------|
| Dashboards | ✅ Lectura | ✅ Lectura | ✅ Lectura | ✅ Lectura | ✅ Lectura | ✅ Lectura |
| Repos de código | ❌ | ✅ Lectura/Escritura | ✅ Lectura/Escritura | ✅ Lectura | ✅ Lectura/Escritura | ✅ Lectura |
| Pipelines CI/CD | ❌ | ✅ Lanzar | ✅ Lanzar | ✅ Configurar | ✅ Configurar | ✅ Lectura |
| Entorno staging | ❌ | ✅ Deploy | ✅ Deploy | ✅ Deploy | ✅ Deploy | ✅ Lectura |
| Entorno producción | ❌ | ❌ | ✅ Lectura | ✅ Deploy | ✅ Deploy | ✅ Lectura |
| Gestión de usuarios | ❌ | ❌ | ❌ | ❌ | ✅ Gestionar | ✅ Lectura |
| Logs de auditoría | ❌ | ❌ | ❌ | ✅ Lectura | ✅ Lectura | ✅ Lectura |
| Configuración de seguridad | ❌ | ❌ | ❌ | ✅ Lectura | ✅ Gestionar | ✅ Lectura |

### Control de Acceso Basado en Atributos (ABAC)

| Atributo | Valores | Efecto sobre el acceso |
|----------|---------|------------------------|
| Departamento | Engineering, Finance, HR, Sales | Restringe a los recursos del departamento |
| Ubicación | Oficina, Remoto, VPN | Remoto requiere VPN para prod |
| Horario | Horario laboral, fuera de horario | Deploy a prod solo en horario laboral |
| Dispositivo | Gestionado, no gestionado | Dispositivos no gestionados bloqueados de prod |
| Nivel de riesgo | Bajo, medio, alto | Riesgo alto requiere autenticación reforzada |

### Gestión de Acceso Privilegiado (PAM)

| Privilegio | Método de acceso | Aprobación | Duración | Registro |
|------------|------------------|------------|----------|----------|
| SSH a producción | Jump host con MFA | Aprobación del manager | 4 horas | Grabación completa de sesión |
| Admin de base de datos | Bastion con MFA | Aprobación de manager + DBA | 2 horas | Log de queries |
| Consola cloud | Cuenta break-glass | Aprobación del CISO | 1 hora | Audit trail completo |
| Admin de Kubernetes | kubectl vía jump host | Aprobación del manager | 4 horas | Log de comandos |
| Root/sudo | Elevación just-in-time | Aprobación de manager + CISO | 1 hora | Log de comandos |

## 3. Gestión de Sesiones

### Configuración de Sesiones

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| Timeout de sesión (activa) | 8 horas | Jornada laboral sin re-autenticación |
| Timeout de sesión (inactiva) | 30 minutos | Logout automático por inactividad |
| Timeout de sesión (privilegiada) | 1 hora | Más corto para sesiones de admin |
| Sesiones concurrentes | 3 máx. | Evita compartir sesiones |
| Almacenamiento de sesión | Cookies HTTP-only, Secure | Evita robo vía XSS |
| Protección CSRF | Cookies SameSite=Strict | Evita ataques CSRF |
| Invalidación de sesión | Al cambiar la contraseña | Fuerza re-autenticación tras el cambio |
| Caducidad de token (API) | 1 hora access, 30 días refresh | Access tokens de vida corta |

### Seguridad de Sesiones

| Control | Implementación | Verificación |
|---------|----------------|--------------|
| Tokens firmados | JWT con RS256 | Verificar firma en cada request |
| Tokens cifrados | JWE para claims sensibles | Descifrar solo en servidor |
| Rotación de refresh token | Nuevo refresh token en cada uso | Detecta robo de tokens |
| Vinculación a dispositivo | Token ligado al fingerprint del dispositivo | Rechazar desde otros dispositivos |
| Vinculación a IP | Token ligado a rango de IP | Rechazar desde IPs inesperadas |
| Revocación de sesión | Lista de revocación consultada | Logout inmediato |

## 4. Aprovisionamiento de Acceso

### Proceso de Onboarding

| Paso | Acción | Responsable | SLA |
|------|--------|-------------|-----|
| 1 | RRHH crea el registro del empleado | RRHH | Antes de la fecha de inicio |
| 2 | IT crea las cuentas | IT | 1 día hábil |
| 3 | El manager solicita el acceso | Manager | 1 día hábil |
| 4 | Acceso aprobado | Data Owner | 2 días hábiles |
| 5 | Acceso aprovisionado | IT | 1 día hábil |
| 6 | Usuario notificado | IT | Mismo día |
| 7 | Acceso registrado | Compliance | 1 día hábil |

### Proceso de Offboarding

| Paso | Acción | Responsable | SLA |
|------|--------|-------------|-----|
| 1 | RRHH notifica la baja | RRHH | En la fecha de baja |
| 2 | El manager confirma el último día | Manager | Mismo día |
| 3 | Acceso revocado | IT | En 24 horas |
| 4 | Dispositivos devueltos | IT | En 3 días |
| 5 | Cuentas desactivadas | IT | En 24 horas |
| 6 | Baja registrada | Compliance | 1 día hábil |
| 7 | Revisión final de acceso | Compliance | 1 semana |

### Proceso de Cambio de Acceso

| Disparador | Acción | Aprobador | SLA |
|------------|--------|-----------|-----|
| Cambio de rol | Revisar y actualizar acceso | Nuevo manager | 3 días hábiles |
| Transferencia de equipo | Quitar acceso del equipo anterior, añadir el nuevo | Nuevo manager | 3 días hábiles |
| Ascenso | Añadir permisos del nuevo rol | Manager + CISO | 5 días hábiles |
| Descenso | Retirar acceso elevado | Manager | 1 día hábil |
| Acceso temporal | Otorgar con fecha de caducidad | Manager + Data Owner | 1 día hábil |

## 5. Revisiones de Acceso

### Calendario de Revisiones

| Alcance | Frecuencia | Revisor | Acción |
|---------|------------|---------|--------|
| Todo el acceso de usuarios | Trimestral | Manager | Retirar acceso sin uso |
| Acceso privilegiado | Mensual | CISO | Verificar necesidad real |
| Cuentas de servicio | Trimestral | Responsable técnico | Verificar que sigue siendo necesaria |
| Acceso externo | Mensual | Sponsor | Verificar contrato activo |
| Cuentas dormidas | Mensual | IT | Desactivar tras 30 días sin uso |
| Cuentas huérfanas | Mensual | IT | Eliminar cuentas sin dueño |

### Checklist de Revisión

| Control | Método | Criterio de aprobación |
|---------|--------|------------------------|
| El usuario sigue empleado | Cruce con RRHH | Todos los usuarios tienen registro activo |
| El acceso coincide con el rol | Comparar permisos con la definición del rol | Sin permisos excesivos |
| Sin cuentas compartidas | Verificar un usuario único por cuenta | Cada cuenta tiene un solo usuario |
| MFA habilitado | Verificar alta en MFA en el IdP | 100% de alta |
| Sin cuentas dormidas | Verificar fecha de último login | Ninguna cuenta inactiva > 30 días |
| Cuentas de servicio documentadas | Verificar el registro de cuentas | Todas tienen dueño y propósito |
| Acceso temporal caducado | Verificar fechas de caducidad | Sin acceso temporal vencido |

## 6. Acceso de API y Servicios

### Autenticación de API

| Tipo de API | Autenticación | Vida del token | Scope | Rate limit |
|-------------|---------------|----------------|-------|------------|
| API pública | OAuth 2.0 (PKCE) | 1 hora access | Scope por cliente | 1000 req/min |
| API interna | mTLS | Vida del certificado | Identidad de servicio | 5000 req/min |
| Servicio a servicio | JWT (RS256) | 1 hora | Scope de servicio | 10000 req/min |
| Webhook | Firma HMAC | Por request | N/A | 100 req/min |
| API de administración | API key + MFA | Rotación cada 90 días | Scope admin | 100 req/min |

### Gestión de API Keys

| Requisito | Implementación | Verificación |
|-----------|----------------|--------------|
| Generación de claves | Aleatoriedad criptográfica, 256 bits | Verificar entropía |
| Almacenamiento | Hasheadas en reposo (bcrypt) | Verificar hash, no texto plano |
| Transmisión | Solo TLS 1.2+ | Verificar que no hay HTTP |
| Rotación | Cada 90 días | Pipeline de rotación automatizada |
| Revocación | Inmediata vía lista de revocación | Verificar propagación |
| Scope | Mínimo privilegio por clave | Auditar scopes trimestralmente |
| Logging | Nunca registrar valores de claves | Buscar patrones de claves en logs |
