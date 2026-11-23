# OWASP Top 10 2025 - Checklist de remediación

Verificaciones de remediación por categoría, ordenadas por prioridad (P0 primero). Contexto completo y ejemplos de código: https://stackpractices.com/es/docs/owasp-top-10-remediation-checklist/

## 1. A01:2025 — Control de Acceso Roto

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Aplica autorización con denegación por defecto en cada ruta, no solo en las sensibles | P0 |
| ☐ | Verifica la propiedad del recurso en el servidor antes de leer/escribir/borrar (check IDOR) | P0 |
| ☐ | Re-verifica la autorización en cada petición — nunca confíes en un rol cacheado en el cliente | P0 |
| ☐ | Usa identificadores no adivinables (UUID) para recursos expuestos en URLs | P1 |
| ☐ | Invalida sesiones al cerrar sesión y tras inactividad | P1 |
| ☐ | Aplica limitación de tasa por usuario y por IP en endpoints sensibles | P1 |
| ☐ | Desactiva el listado de directorios e índices públicos de archivos | P1 |
| ☐ | Valida los destinos de redirección contra una lista permitida | P1 |
| ☐ | Para SSRF: lista permitida de dominios salientes; bloquea rangos IP internos y esquemas `file://`/`gopher://` | P0 |
| ☐ | Para SSRF: desactiva el seguimiento de redirecciones en peticiones salientes del servidor | P1 |
| ☐ | Registra cada acceso denegado con usuario, recurso y motivo | P2 |

## 2. A02:2025 — Configuración de Seguridad Incorrecta

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Elimina o rota cada credencial por defecto (bases de datos, paneles de admin, brokers de mensajes) | P0 |
| ☐ | Apaga el modo debug y las páginas de error con traza en producción | P0 |
| ☐ | Cierra el almacenamiento en la nube al público (buckets S3, blobs) y limita IAM al mínimo privilegio | P0 |
| ☐ | Envía las cabeceras de seguridad de abajo en cada respuesta | P1 |
| ☐ | Quita endpoints, funciones y dependencias sin usar del artefacto desplegado | P1 |
| ☐ | Restringe CORS a orígenes explícitos — nunca `*` con credenciales | P1 |
| ☐ | Separa la configuración por entorno; los secretos de producción nunca llegan a dev/staging | P1 |
| ☐ | Programa escaneos automáticos de configuración (Prowler, Scout Suite, Trivy) y revisa resultados cada semana | P2 |
| ☐ | Documenta cada desviación intencional respecto a las líneas base de endurecimiento | P2 |

## 3. A03:2025 — Fallas en la Cadena de Suministro de Software

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Genera un SBOM por cada artefacto de release (CycloneDX o SPDX) | P1 |
| ☐ | Escanea dependencias en CI en cada PR; bloquea merges con CVE críticos | P0 |
| ☐ | Fija versiones exactas — nada de rangos flotantes en dependencias de producción | P0 |
| ☐ | Verifica la procedencia de paquetes: lockfiles commiteados, checksums o firmas comprobadas | P1 |
| ☐ | Restringe de qué registros puede descargar el build; usa un proxy interno para registros públicos | P1 |
| ☐ | Protege el pipeline: commits firmados o ramas protegidas, secretos fuera de los logs de CI | P1 |
| ☐ | Elimina dependencias sin usar — cada paquete innecesario es superficie de ataque | P1 |
| ☐ | Sigue las fechas de fin de vida de tus frameworks y planifica migraciones antes de que venzan | P2 |
| ☐ | Suscríbete a avisos de seguridad de tu stack crítico (avisos de GitHub, listas de vendors) | P2 |
| ☐ | Revisa las dependencias transitivas en cada cambio de versión mayor | P2 |

## 4. A04:2025 — Fallas Criptográficas

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Exige TLS 1.2+ en todas partes; desactiva SSLv3, TLS 1.0 y 1.1 | P0 |
| ☐ | Cifra datos sensibles en reposo (AES-256-GCM o equivalentes gestionados por el proveedor) | P0 |
| ☐ | Hashea contraseñas con Argon2id o bcrypt — nunca hashes rápidos como SHA-256 a secas | P0 |
| ☐ | Saca cada secreto del código fuente hacia un gestor de secretos | P0 |
| ☐ | Rota claves en calendario y tras cualquier sospecha de exposición | P1 |
| ☐ | Clasifica los datos para saber qué necesita cifrado de verdad (no cifres todo a ciegas) | P1 |
| ☐ | Activa HSTS con preload en propiedades públicas | P1 |
| ☐ | No inventes criptografía — usa librerías auditadas con sus parámetros recomendados | P1 |
| ☐ | Audita dónde usas aleatoriedad; los tokens de seguridad necesitan un CSPRNG | P1 |
| ☐ | Define la custodia de claves: quién puede descifrar y cómo queda registrado | P2 |

## 5. A05:2025 — Inyección

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Parametriza cada consulta a base de datos — cero SQL construido con strings | P0 |
| ☐ | Audita el uso del ORM buscando vías de escape a SQL crudo (`raw()`, `extra()`, queries plantilla) | P0 |
| ☐ | Ejecuta subprocesos con `shell=False` y arrays de argumentos, nunca strings interpolados | P0 |
| ☐ | Valida la entrada contra listas permitidas (tipo, longitud, formato) en el límite de confianza | P1 |
| ☐ | Escapa la salida según su contexto — HTML, JS, URL y CSS son contextos distintos | P1 |
| ☐ | Limita resultados de consultas (`LIMIT`/`OFFSET`) para que una inyección exitosa no vacíe la tabla | P1 |
| ☐ | Da a los usuarios de base de datos privilegios mínimos; la app web no debería poder hacer `DROP` | P1 |
| ☐ | Alerta sobre errores de sintaxis SQL en logs de producción — son firma de sondeo | P2 |
| ☐ | Convierte los payloads de inyección de tu pentest en pruebas de regresión | P2 |

## 6. A06:2025 — Diseño Inseguro

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Modela amenazas en funciones que mueven dinero, datos o permisos antes de construirlas | P1 |
| ☐ | Escribe casos de abuso junto a las historias de usuario (¿cómo usaría esto un atacante?) | P1 |
| ☐ | Limita la tasa de toda acción que cuesta dinero o recursos — registro, reset, búsqueda, exportación | P0 |
| ☐ | Separa los datos de cada tenant a nivel de arquitectura, no solo con un `WHERE` | P1 |
| ☐ | Diseña flujos que cambian estado con verificación reforzada en los pasos sensibles | P1 |
| ☐ | Falla en cerrado: cuando un check no puede ejecutarse, deniega en vez de permitir | P0 |
| ☐ | Acota operaciones recuperables — intentos ilimitados de reset de contraseña son un bug de diseño | P1 |
| ☐ | Registra eventos de negocio, no solo técnicos (quién transfirió qué y cuándo) | P2 |
| ☐ | Revisa diseños pensando en minimización de datos — no puedes filtrar lo que nunca recolectaste | P2 |

## 7. A07:2025 — Fallas de Autenticación

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Ofrece MFA en todas partes; exígelo para admins y acciones sensibles | P0 |
| ☐ | Compara contraseñas contra listas de filtraciones en registro y reset | P1 |
| ☐ | Limita la tasa en login y recuperación; añade demoras progresivas o bloqueo | P0 |
| ☐ | Regenera los IDs de sesión al hacer login, cambiar privilegios y cerrar sesión | P0 |
| ☐ | Mantén los tokens de sesión largos, aleatorios y revocables desde el servidor | P1 |
| ☐ | Haz los tokens de reset de un solo uso, de corta vida y ligados a la cuenta | P1 |
| ☐ | Define expiraciones de sesión explícitas (inactividad y absoluta) y respétalas en el servidor | P1 |
| ☐ | Alerta sobre patrones de credential stuffing — muchos fallos de login repartidos en muchas cuentas | P1 |
| ☐ | Registra cada evento de autenticación con su resultado; el silencio aquí te impide detectar A09 | P2 |
| ☐ | No reinventes — usa la maquinaria de sesiones/autenticación de tu framework | P2 |

## 8. A08:2025 — Fallas de Integridad de Software o Datos

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Firma los artefactos de release y verifica las firmas al desplegar | P1 |
| ☐ | Añade subresource integrity (SRI) a cada etiqueta de script de terceros | P1 |
| ☐ | Trata la deserialización como entrada no confiable; evita del todo la deserialización nativa de objetos | P0 |
| ☐ | Verifica las firmas de webhooks antes de actuar sobre ellos | P0 |
| ☐ | Usa imágenes de contenedor inmutables fijadas por digest — nada de `latest` en producción | P1 |
| ☐ | Protege los espacios de ramas y tags para que las refs de release no se muevan en silencio | P1 |
| ☐ | Registra la procedencia del build (atestaciones estilo SLSA) en los binarios de release | P2 |
| ☐ | Detecta deriva: alerta cuando lo que corre difiere de los releases firmados | P2 |

## 9. A09:2025 — Fallas de Registro y Alerta de Seguridad

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Registra fallos de autenticación, autorización y validación de entrada con contexto | P0 |
| ☐ | Centraliza los logs fuera de los hosts de la app (un atacante que posee la máquina posee sus logs) | P0 |
| ☐ | Alerta sobre los patrones que importan: fuerza bruta, cambios de privilegios, egreso inusual | P1 |
| ☐ | Incluye actor, marca de tiempo, IP de origen y resultado en cada evento de seguridad | P1 |
| ☐ | Protege la integridad de los logs — almacenamiento append-only o WORM para pistas de auditoría | P1 |
| ☐ | Sanitiza lo que se escribe en los logs para prevenir inyección de logs y entradas falsificadas | P1 |
| ☐ | Define y aplica una retención acorde a tus obligaciones (90+ días es lo típico) | P1 |
| ☐ | Prueba las alertas de extremo a extremo — una regla que nunca saltó no está verificada | P2 |
| ☐ | Programa revisión de logs: automática a diario, humana en una cadencia real | P2 |

## 10. A10:2025 — Manejo Incorrecto de Condiciones Excepcionales

| Estado | Verificación | Prioridad |
|---|---|---|
| ☐ | Falla en cerrado en rutas relevantes para seguridad — un error durante un check significa denegar | P0 |
| ☐ | Nunca tragues excepciones en silencio; registra con contexto suficiente para depurar después | P1 |
| ☐ | Pon timeout a cada llamada saliente — una espera sin límite es un DoS por agotamiento | P0 |
| ☐ | Devuelve errores genéricos al cliente; los internos (trazas, hostnames) quedan en el servidor | P1 |
| ☐ | Maneja el fallo parcial de forma explícita: ¿qué pasa si el cobro salió pero el email no? | P1 |
| ☐ | Acota el uso de recursos — tamaños de entrada, reintentos, profundidad de colas, uploads | P1 |
| ☐ | Prueba los caminos de error en staging, incluidos los que "nunca pasan" | P1 |
| ☐ | Alerta sobre picos de tasa de errores; una avalancha repentina de 500 suele ser firma de ataque | P2 |
