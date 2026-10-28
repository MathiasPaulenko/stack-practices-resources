# Scripts de Bash para AWS CLI

Scripts complementarios de la receta [Scripts de Bash para AWS CLI](https://stackpractices.com/es/recipes/bash-aws-cli-scripts/) en StackPractices.

Cada archivo `.sh` es autocontenido: ajusta las variables de arriba y ejecútalo. Todos asumen AWS CLI v2 configurado (`aws configure`, variables de entorno o SSO) y usan `set -euo pipefail` para que los fallos detengan la ejecución en vez de aplicar cambios a medias.

## Prerequisitos

- AWS CLI v2 (`aws --version`)
- Credenciales válidas para la cuenta objetivo (usuario IAM, rol de instancia o `aws sso login`)
- `jq` — requerido por `tag-compliance-audit.sh` y `multi-account-deploy.sh`
- `date` de GNU — los snippets de retención/corte usan `date -d`; en macOS instala coreutils (`brew install coreutils`, y usa `gdate`) o adapta a `date -v-30d`

## Scripts

| Archivo | Qué hace |
| --- | --- |
| `provision-ec2-instance.sh` | Lanza una instancia EC2, espera a `running`, imprime la IP pública |
| `list-ec2-instances.sh` | Tabla de todas las instancias: ID, estado, tipo, IP, tag Name |
| `ephemeral-vpc.sh` | Crea un VPC + subnet etiquetados y los elimina al salir (exporta `KEEP=1` para conservarlos) |
| `s3-bucket-setup.sh` | Crea un bucket (maneja el caso `us-east-1`), habilita versionado, aplica ciclo de vida por niveles, audita objetos viejos |
| `s3-sync-directory.sh` | Espeja un directorio local a S3 con `--delete` y clase de almacenamiento |
| `stop-ec2-by-tag.sh` | Detiene todas las instancias con `Environment=dev` (cambia a `start-instances` para el inverso) |
| `iam-user-audit.sh` | Vuelca access keys, políticas adjuntas y grupos de cada usuario IAM |
| `rds-snapshot-backup.sh` | Crea snapshot RDS, espera, poda snapshots anteriores a la retención |
| `tag-compliance-audit.sh` | Reporta instancias corriendo y buckets sin tags requeridos (necesita `jq`) |
| `ebs-snapshot-rotation.sh` | Saca snapshot de volúmenes `Backup=true`, elimina snapshots más viejos que N días |
| `cleanup-unattached-ebs.sh` | Elimina cada volumen EBS desconectado (`available`) — dry-run primero |
| `cost-explorer-report.sh` | Gasto diario por servicio de los últimos 30 días |
| `cloudwatch-dashboard.sh` | Publica un dashboard de CloudWatch desde un body JSON |
| `multi-account-deploy.sh` | Itera cuentas dev/staging/prod con `assume-role` y actualiza una Lambda (necesita `jq`) |

## Notas de seguridad

- Los scripts que eliminan o modifican recursos soportan una pasada en seco manual: comenta la llamada de borrado o usa `--dry-run` donde la API lo permita (llamadas mutantes de EC2).
- Prueba primero contra una cuenta no productiva.
- Nunca embebas access keys en scripts — usa roles IAM, variables de entorno o `aws sts assume-role`.
