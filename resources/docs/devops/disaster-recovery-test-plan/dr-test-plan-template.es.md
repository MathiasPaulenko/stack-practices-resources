# Plantilla de Plan de Pruebas de Recuperaci?n ante Desastres

Completa cada marcador antes de la ventana de prueba. Adapta objetivos y tiempos al servicio; no son valores predeterminados.

# Plan de Prueba de Recuperación ante Desastres: `<Nombre del Servicio>`

## 1. Objetivos de la Prueba

| Objetivo | Meta | medición |
|----------|------|----------|
| Objetivo de Tiempo de Recuperación (RTO) | `<meta aprobada>` | Inicio: `<evento>`; detener cuando: `<transacción crítica completada>` |
| Objetivo de Punto de Recuperación (RPO) | `<meta aprobada>` | Comparar la última marca transaccional recuperada con el límite de la falla |
| Integridad de datos | `<umbral definido>` | Comprobar filas y reglas de negocio requeridas; anotar exclusiones |
| Comunicación | `<ventana aprobada>` | Avisar a las personas responsables antes de iniciar |

## 2. Alcance y Suposiciones

### Dentro del alcance
- Conmutación de la base de datos y restauración desde una copia de seguridad
- Nuevo despliegue de la aplicación en la región de DR
- Cambio de DNS y enrutamiento de tráfico
- Validación de flujos críticos mediante pruebas básicas en un entorno de recuperación aislado

### Fuera del alcance
- Dependencias de terceros que no se probarán expresamente (indica cada exclusión y su responsable)
- Fallas completas de un centro de datos físico (prueba basada en la nube)
- Escenarios de aislamiento completo de red

### Supuestos
- Hay un punto de restauración disponible en la región de destino y se confirmó su estado
- El entorno de recuperación dispone de capacidad, rutas de red y accesos requeridos
- Los datos de prueba y sus rutas están aislados de las escrituras de clientes
- Las personas responsables y quien puede detener la prueba estarán disponibles

## 3. Escenarios de Prueba

### Escenario A: falla completa de la región primaria

**Disparador:** indisponibilidad simulada de la región primaria mediante el mecanismo aprobado para este entorno.

**Pasos:**
1. **Declarar desastre** (0:00) — Ingeniero líder anuncia prueba de DR en canal de incidente
2. **Restaurar la base de datos** (0:30) — Restaurar desde una instantánea verificada y disponible en la región de DR
3. **Desplegar aplicaciones** (1:00) — Desplegar la aplicación en el clúster de DR
4. **Actualizar DNS** (1:30) — Cambiar tráfico a balanceador de carga de DR
5. **Validar** (2:00) — Ejecutar pruebas de humo y verificar la integridad de los datos
6. **Medir RTO** — Registrar tiempo desde declaración hasta validación exitosa

### Escenario B: corrupción de base de datos

**Disparador:** la base de datos primaria contiene un registro de prueba conocido o una copia aislada con corrupción que requiere recuperación a un punto en el tiempo. No inyectes corrupción en datos de producción para este ejercicio.

**Pasos:**
1. Identificar punto de corrupción desde alertas de monitoreo
2. Elegir un punto anterior al marcador de corrupción de prueba y registrar su ID de transacción o número de secuencia del registro
3. Restaurar a ese punto y comparar filas clave y marcas de agua transaccionales
4. Promover instancia restaurada a primaria
5. Redirigir tráfico de aplicación

## 4. Ejecución de la Prueba

### Checklist Pre-Prueba

| Elemento | Estado | Responsable |
|------|--------|-------------|
| Punto de restauración disponible en la región de destino | [ ] | DBA |
| Entorno de DR y ruta de prueba de la aplicación aislados | [ ] | Plataforma |
| Definiciones del cronómetro RTO/RPO y criterios aprobados | [ ] | Dueño del servicio |
| Criterios de parada y responsable de reversión confirmados | [ ] | Líder de prueba |
| Procedimientos operativos impresos o accesibles sin conexión | [ ] | SRE |
| Personas interesadas notificadas | [ ] | Líder de incidentes |
| Procedimiento de reversión confirmado | [ ] | SRE |
| Dashboards de monitoreo listos | [ ] | Observabilidad |

### Línea de Tiempo de Ejecución

Los tiempos siguientes son un ejemplo. Sustitúyelos por estimaciones obtenidas en un ensayo y por los objetivos aprobados del servicio; no son una garantía de recuperación.

| Tiempo | Actividad | Resultado Esperado |
|--------|-----------|-------------------|
| T+0:00 | Declarar inicio de prueba | Canal de incidente notificado |
| T+0:05 | Iniciar restauración de base de datos | Trabajo de restauración RDS iniciado |
| T+1:00 | Base de datos disponible | Prueba de conexión exitosa |
| T+1:30 | Desplegar aplicación | Todos los pods saludables |
| T+2:00 | Cambio de DNS | tráfico llegando a región de DR |
| T+2:30 | Pruebas de humo | 100% de los flujos aprobados |
| T+3:00 | verificación de integridad de datos | Conteo de transacciones coincide con fuente |
| T+4:00 | medición de RTO | Registrar actual vs meta |

### Procedimiento de Rollback

Si cualquier paso crítico falla:
1. Detén nuevas acciones y registra las rutas actuales de tráfico y escritura
2. Pide a quien coordina y a la persona responsable de la base de datos que confirmen qué entorno tiene los datos autoritativos
3. Reconcilia las escrituras antes de devolver tráfico a la región primaria
4. Conserva los recursos de DR y las evidencias hasta la revisión posterior
5. Trata cualquier impacto en clientes o datos como un incidente y programa otra prueba tras corregir las causas

## 5. Verificación de Integridad de Datos

```sql
-- comparación de conteo de transacciones
SELECT 'primary' as source, COUNT(*) as tx_count FROM orders
UNION ALL
SELECT 'dr', COUNT(*) FROM dr_orders;

-- Compara las mismas claves y columnas de negocio en ambos sentidos.
-- EXCEPT está disponible en PostgreSQL y SQL Server; adapta columnas y tipos.
SELECT COUNT(*) AS filas_que_faltan_en_dr
FROM (
  SELECT payment_id, status, amount_cents, created_at FROM payments
  EXCEPT
  SELECT payment_id, status, amount_cents, created_at FROM dr_payments
) AS faltan_en_dr;

SELECT COUNT(*) AS filas_adicionales_en_dr
FROM (
  SELECT payment_id, status, amount_cents, created_at FROM dr_payments
  EXCEPT
  SELECT payment_id, status, amount_cents, created_at FROM payments
) AS sobran_en_dr;

-- Un timestamp solo aproxima el RPO; prefiere una marca duradera y específica del motor.
SELECT MAX(created_at) FROM orders;
```

| Verificación | Primario | DR | Coincide |
|--------------|----------|-----|----------|
| Conteo de transacciones | ______ | ______ | [ ] |
| Filas distintas en cualquiera de los sentidos | ______ | ______ | [ ] |
| último timestamp | ______ | ______ | [ ] |

## 6. Reporte Post-Prueba

### Resumen de Resultados

| Métrica | Meta | Actual | Estado |
|---------|------|--------|--------|
| RTO | `<meta aprobada>` | ______ | Aprobado / Fallido / No probado |
| RPO | `<meta aprobada>` | ______ | Aprobado / Fallido / No probado |
| Integridad de datos | `<umbral definido>` | ______ | Aprobado / Fallido / No probado |
| Pruebas básicas | `<flujos críticos>` | ______ | Aprobado / Fallido / No probado |

### Problemas Encontrados

| Problema | Severidad | Responsable | Fecha límite de corrección |
|----------|-----------|-------------|---------------------------|
| ______ | crítica / Alta / Media / Baja | ______ | ______ |

Para cada hallazgo, adjunta el resultado esperado y observado, el ID de evidencia, el impacto, la persona responsable, la fecha límite y el escenario que se repetirá. Marca como excluidas o bloqueadas las comprobaciones que no se ejecutaron; no las cuentes como aprobadas.

### Lecciones Aprendidas

- Lo que funcionó bien:
- Lo que tomó más tiempo de lo esperado:
- Lo que falló inesperadamente:
- Lo que debería automatizarse:

### Aprobación

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Líder de Prueba | ______ | ______ | ______ |
| Gerente de Ingeniería | ______ | ______ | ______ |
| Compliance (si aplica) | ______ | ______ | ______ |
