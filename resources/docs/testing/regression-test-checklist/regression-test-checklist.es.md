# Checklist de Pruebas de Regresión — `<Versión del Release>`

## Información del Release

| Campo | Valor |
|-------|-------|
| Versión del Release | v2.5.0 |
| Fecha del Release | 2026-07-05 |
| Release Manager | <Nombre> |
| Resumen de Cambios | Nuevo flujo de reembolso de pagos, upgrade de Node.js 18→20, migración de esquema de base de datos |
| Nivel de Riesgo | Medio (migración de esquema + upgrade de dependencias) |
| Plan de Rollback | Volver a v2.4.1, ejecutar el script de rollback de la migración |

## 1. Comprobaciones Pre-Deploy

### 1.1. Build y CI

- [ ] Todos los checks de CI pasan (lint, type-check, unit tests, integration tests)
- [ ] La cobertura de tests alcanza el umbral (>= 80% de líneas, >= 70% de branches)
- [ ] No se introdujeron tests flaky nuevos
- [ ] El build compila sin warnings
- [ ] El tamaño del bundle está dentro del presupuesto (actual: 2.3 MB, límite: 3 MB)
- [ ] La imagen Docker se construye correctamente
- [ ] El escaneo de seguridad pasa (sin vulnerabilidades nuevas)

### 1.2. Calidad de Código

- [ ] Todos los PRs revisados y aprobados
- [ ] Sin comentarios TODO/FIXME en los archivos modificados
- [ ] Breaking changes documentados en el CHANGELOG
- [ ] Los contract tests de API pasan (sin breaking changes detectados)
- [ ] Migración de base de datos probada en staging
- [ ] Script de rollback de la migración probado

### 1.3. Preparación del Entorno

- [ ] El entorno de staging coincide con la configuración de producción
- [ ] Backup de la base de datos tomado antes de la migración
- [ ] Feature flags configurados para las features nuevas
- [ ] Variables de entorno actualizadas en producción
- [ ] Caché del CDN invalidada para los assets estáticos
- [ ] Dashboards de monitoreo activos
- [ ] Umbrales de alerta ajustados para las métricas nuevas

### 1.4. Comunicación

- [ ] Release notes preparadas
- [ ] Equipos downstream notificados de los cambios de API
- [ ] Ingeniero on-call informado de los cambios
- [ ] Ventana de mantenimiento programada (si hace falta)
- [ ] Stakeholders notificados del horario del deploy

## 2. Comprobaciones de Despliegue

### 2.1. Migración de Base de Datos

- [ ] La migración corre correctamente en staging
- [ ] El rendimiento de la migración es aceptable (< 5 minutos)
- [ ] No se detectó pérdida de datos (los conteos de filas antes/después coinciden)
- [ ] Script de rollback de la migración probado
- [ ] Backup de la base de datos verificado

### 2.2. Despliegue de la Aplicación

- [ ] El despliegue blue/green conmuta correctamente
- [ ] El endpoint de health check devuelve 200
- [ ] No hay picos de errores nuevos en los logs
- [ ] Los tiempos de respuesta están dentro del rango normal
- [ ] El pool de conexiones de base de datos está estable
- [ ] Caché precalentada (si aplica)

## 3. Smoke Tests Post-Deploy

### 3.1. Recorridos Críticos del Usuario

| Recorrido | Pasos | Esperado | Estado |
|-----------|-------|----------|--------|
| Login de usuario | Ingresar credenciales válidas, hacer clic en login | Redirigido al dashboard | [ ] |
| Registro de usuario | Completar el formulario, enviar, verificar email | Cuenta creada, email enviado | [ ] |
| Explorar productos | Navegar a la lista de productos | Productos mostrados con imágenes | [ ] |
| Agregar al carrito | Hacer clic en "Add to Cart" en un producto | El contador del carrito incrementa | [ ] |
| Checkout | Completar el flujo de checkout | Orden creada, pago procesado | [ ] |
| Seguimiento de orden | Ver el estado de la orden | Estado mostrado correctamente | [ ] |
| Reset de contraseña | Solicitar reset, hacer clic en el enlace del email | Contraseña actualizada correctamente | [ ] |
| Búsqueda | Ingresar una consulta, enviar | Resultados mostrados | [ ] |

### 3.2. Salud de la API

| Endpoint | Método | Estado Esperado | Tiempo de Respuesta | Estado |
|----------|--------|-----------------|---------------------|--------|
| /health | GET | 200 | < 50ms | [ ] |
| /api/v1/users | GET | 200 | < 200ms | [ ] |
| /api/v1/products | GET | 200 | < 300ms | [ ] |
| /api/v1/orders | GET | 200 | < 300ms | [ ] |
| /api/v1/payments | POST | 201 | < 500ms | [ ] |
| /api/v1/payments/{id}/refund | POST | 201 | < 500ms | [ ] |

### 3.3. Infraestructura

| Comprobación | Esperado | Estado |
|--------------|----------|--------|
| Conexiones de base de datos | < 80% del pool | [ ] |
| Memoria de Redis | < 80% del límite | [ ] |
| Uso de CPU | < 70% promedio | [ ] |
| Uso de memoria | < 80% del límite | [ ] |
| Espacio en disco | > 20% libre | [ ] |
| Tasa de errores | < 0.1% de los requests | [ ] |
| Latencia p95 | < 500ms | [ ] |

### 3.4. Monitoreo y Alertas

- [ ] No se dispararon alertas críticas post-deploy
- [ ] Tasa de errores dentro del rango normal (comparar con la baseline pre-deploy)
- [ ] Latencia dentro del rango normal
- [ ] No hay patrones de error nuevos en los logs
- [ ] Monitoreo sintético pasando
- [ ] Monitoreo de uptime en verde

## 4. Pruebas de Regresión Específicas por Feature

### 4.1. Flujo de Reembolso de Pagos (Feature Nueva)

- [ ] El admin puede iniciar un reembolso desde la página de detalle de la orden
- [ ] El reembolso parcial funciona (reembolsar 50% del total de la orden)
- [ ] El reembolso total funciona (reembolsar 100% del total de la orden)
- [ ] El reembolso dispara una notificación por email al usuario
- [ ] El reembolso aparece en el historial de la orden
- [ ] El reembolso actualiza el dashboard de reportes financieros
- [ ] El reembolso falla sin romperse si el proveedor de pagos está caído
- [ ] Se crea una entrada de audit log del reembolso con ID de admin y timestamp

### 4.2. Upgrade de Node.js 20

- [ ] Todos los endpoints de la API responden correctamente
- [ ] Los background jobs procesan sin errores
- [ ] Las conexiones WebSocket están estables
- [ ] Las subidas de archivos funcionan (multipart form data)
- [ ] La generación de PDF funciona (puppeteer)
- [ ] No hay warnings de deprecación en los logs

### 4.3. Migración de Esquema de Base de Datos

- [ ] Las órdenes existentes se muestran correctamente (columna `refund_status` añadida)
- [ ] Las órdenes nuevas incluyen el campo `refund_status`
- [ ] Las consultas de órdenes se mantienen dentro de la baseline (< 200ms)
- [ ] Los índices de la columna nueva son efectivos
- [ ] No hay registros huérfanos por la migración

## 5. Verificación de Rollback

### 5.1. Disparadores de Rollback

| Condición | Acción |
|-----------|--------|
| Tasa de errores > 1% durante 5 minutos | Rollback inmediato |
| Latencia p95 > 2s durante 5 minutos | Rollback inmediato |
| Alerta crítica disparada | Evaluar, rollback si está relacionada con el deploy |
| Health check fallando durante 2 minutos | Rollback inmediato |
| Corrupción de datos detectada | Rollback, restaurar desde backup |

### 5.2. Pasos del Rollback

- [ ] Revertir la aplicación a la versión anterior (v2.4.1)
- [ ] Ejecutar el script de rollback de la migración de base de datos
- [ ] Verificar que el health check devuelve 200
- [ ] Verificar que los recorridos críticos del usuario funcionan
- [ ] Verificar que no hubo pérdida de datos por el rollback
- [ ] Notificar a los stakeholders del rollback
- [ ] Crear un postmortem del deploy fallido

### 5.3. Prueba de Rollback (Pre-Release)

- [ ] Rollback probado en staging
- [ ] Tiempo de rollback medido (objetivo: < 10 minutos)
- [ ] Consistencia de datos verificada después del rollback
- [ ] La aplicación funciona correctamente después del rollback

## 6. Sign-Off

| Rol | Nombre | Aprobación | Fecha |
|-----|--------|------------|-------|
| Release Manager | | [ ] Aprobado | |
| Tech Lead | | [ ] Aprobado | |
| QA Lead | | [ ] Aprobado | |
| SRE / On-Call | | [ ] Aprobado | |
| Product Manager | | [ ] Aprobado | |
