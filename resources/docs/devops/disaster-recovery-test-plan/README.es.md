# Plan de Pruebas de Recuperación ante Desastres — Kit Compañero

Archivos independientes de la plantilla [Plan de Pruebas de Recuperación ante Desastres](https://stackpractices.com/es/docs/disaster-recovery-test-plan/) en StackPractices. Todo está pensado para copiarse a tu propio repositorio y adaptarse.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `dr-test-plan-template.md` | Plan de pruebas de seis secciones: objetivos, alcance, escenarios, cronología de ejecución, integridad de datos e informe post-prueba con firmas |
| `dr_test_runner.py` | Restaura un snapshot RDS ya disponible en la región de DR, prueba una URL de aplicación separada, compara conteos, registra el RTO tras las pruebas y deja el RPO sin calcular |
| `game-day.sh` | Simulacros controlados de fallas en Kubernetes, con simulación predeterminada, ejecución explícita, contexto identificado y limpieza |
| `dependency-checks.sh` | Verificaciones de DNS, CDN y circuit breaker de APIs externas para ejecutar tras el cambio de tráfico |
| `integrity-checks.sql` | Consultas PostgreSQL de informe sobre métricas de replicación exportadas y resultados registrados de pruebas DR |
| `dr-test-calendar.md` | Rotación trimestral de escenarios con reglas de cadencia y hoja de seguimiento |

## Uso

Configura `KUBE_CONTEXT` con un clúster de pruebas dedicado. El primer comando solo simula; añade `--execute` después de revisar el destino y el alcance. El escenario `full` también requiere `PRIMARY_REGION` y una confirmación escrita. El escenario `disk` requiere un `FILL_SIZE` elegido para el sistema de archivos de prueba.

```bash
KUBE_CONTEXT="sustituye-por-el-contexto-de-prueba" ./game-day.sh --scenario network
KUBE_CONTEXT="sustituye-por-el-contexto-de-prueba" ./game-day.sh --scenario network --execute
```


```bash
# Verificación de sintaxis antes de ejecutar nada destructivo
bash -n game-day.sh

# Verificación de sintaxis en Python
python -m py_compile dr_test_runner.py
```

**Advertencia:** `game-day.sh --scenario full` acordona y drena todos los nodos con la etiqueta de región primaria. Ejecútalo solo en clusters que puedas permitirte tumbar, y nunca como primer ejercicio.

Antes de ejecutar `DRTestRunner`, copia el snapshot de RDS a la región de destino y espera a que esté disponible. Proporciona credenciales de AWS, el grupo de subredes de destino, una URL de prueba aislada y las URL de conexión mediante configuración aprobada o un gestor de secretos. El ejecutor solo compara conteos; no calcula el RPO. `psql` debe estar en PATH y `kubectl` debe apuntar a un clúster aprobado para el simulacro.

Fuente: [stackpractices.com/es/docs/disaster-recovery-test-plan](https://stackpractices.com/es/docs/disaster-recovery-test-plan/)
