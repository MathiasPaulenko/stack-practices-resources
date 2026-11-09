# Plan de Pruebas de Recuperación ante Desastres — Kit Compañero

Archivos independientes de la plantilla [Plan de Pruebas de Recuperación ante Desastres](https://stackpractices.com/es/docs/disaster-recovery-test-plan/) en StackPractices. Todo está pensado para copiarse a tu propio repositorio y adaptarse.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `dr-test-plan-template.md` | Plan de pruebas de seis secciones: objetivos, alcance, escenarios, cronología de ejecución, integridad de datos e informe post-prueba con firmas |
| `dr_test_runner.py` | Runner con boto3 que restaura un snapshot de RDS en la región de DR, ejecuta smoke tests, verifica la integridad de datos y mide el RTO real |
| `game-day.sh` | Script de ingeniería del caos con escenarios `network`, `disk`, `cpu` y `full` sobre un cluster de Kubernetes |
| `dependency-checks.sh` | Verificaciones de DNS, CDN y circuit breaker de APIs externas para ejecutar tras el cambio de tráfico |
| `integrity-checks.sql` | Consultas de conteo de transacciones, checksums, lag de replicación y seguimiento de RTO/RPO |
| `dr-test-calendar.md` | Rotación trimestral de escenarios con reglas de cadencia y hoja de seguimiento |

## Uso

```bash
# Verificación de sintaxis antes de ejecutar nada destructivo
bash -n game-day.sh

# Verificación de sintaxis en Python
python -m py_compile dr_test_runner.py
```

**Advertencia:** `game-day.sh --scenario full` acordona y drena todos los nodos con la etiqueta de región primaria. Ejecútalo solo en clusters que puedas permitirte tumbar, y nunca como primer ejercicio.

`DRTestRunner` necesita credenciales de AWS con permiso para restaurar snapshots de RDS en la región de DR, `psql` en el PATH para la consulta de integridad y `kubectl` configurado para los escenarios de game day.

Fuente: [stackpractices.com/es/docs/disaster-recovery-test-plan](https://stackpractices.com/es/docs/disaster-recovery-test-plan/)
