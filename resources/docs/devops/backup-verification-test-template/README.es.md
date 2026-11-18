# Plantilla de Prueba de Verificación de Backups — Companion

Registro rellenable de verificación más implementaciones ejecutables:

- `backup-verification-test-template.md` — registro de prueba para rellenar (identificación, alcance/objetivos, procedimiento de restauración, checklist de validación, resumen de resultados, registro de problemas).
- `postgres-restore-verify.sh` — script ejecutable de restauración y verificación PostgreSQL: crea una DB desechable, restaura el dump, verifica conteos de filas, constraints e índices, ejecuta una query de humo y limpia al final.
- `rto-rpo-worksheet.txt` — hoja de medición RTO/RPO con ejemplo completado (timeline de restauración, ventana de pérdida de datos, aprobado/fallido contra objetivos, problemas y remediación).

Fuente: https://stackpractices.com/es/docs/backup-verification-test-template/

Adapta rutas, hosts y umbrales antes de ejecutar el script — y restaura siempre en un entorno aislado, nunca en producción.
