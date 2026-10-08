# Plantilla de Checklist de Desmantelamiento de Sistemas

Kit operativo para retirar un servicio de producción sin romper a los
consumidores downstream. Acompaña a la guía en
<https://stackpractices.com/es/docs/system-decommissioning-checklist-template/>.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `decommissioning-checklist.md` | La checklist completa de 7 fases: descubrimiento, manejo de datos, eliminación de dependencias, apagado, limpieza, documentación y verificación. Cópiala en tu wiki o issue tracker y rellena los placeholders. |
| `decommissioning-notification.txt` | Email de notificación para enviar en T-30 (y reenviar en T-14 / T-3). |
| `post-decommissioning-audit.md` | La checklist de auditoría a los 30 días — ejecútala un ciclo de facturación completo después del apagado. |
| `verify-remaining-resources.sh` | Script Bash que comprueba DNS, EC2, RDS, S3, ACM y CloudWatch en busca de restos etiquetados con el nombre del servicio. Extiéndelo para tu stack. |

## Orden sugerido

1. Rellena `decommissioning-checklist.md` empezando por la sección 1
   (Descubrimiento). No te la saltes — todo incidente de desmantelamiento
   empieza con una dependencia sin mapear.
2. Envía `decommissioning-notification.txt` en T-30, reenvíala en T-14 y T-3.
3. Para el servicio en staging, vigila 24-48 horas, luego producción.
4. Durante la ventana de 30 días, ejecuta `verify-remaining-resources.sh`
   semanalmente:

   ```bash
   SERVICE_NAME=mi-servicio AWS_REGION=us-east-1 ./verify-remaining-resources.sh
   ```

5. En T+30, completa `post-decommissioning-audit.md` y archívala como evidencia.
6. En T+90, purga los artefactos conservados según tu política de retención.

## Notas

- Conserva una snapshot restaurable (repo archivado, exportación de config,
  volcado de datos) durante 90 días — hace barato un reinicio temporal si
  aparece un consumidor oculto.
- "Archivar" significa una restauración verificada, no una copia. Prueba un
  archivo en T-14.
