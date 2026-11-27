# Gestión de Certificados SSL — Kit complementario

Material complementario de la [Plantilla de Gestión de Certificados SSL](https://stackpractices.com/es/docs/ssl-certificate-management-template/).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `scripts/certbot-renew.sh` | Renovación certbot con deploy hook + alerta a Slack en falla |
| `scripts/certbot-wildcard.sh` | Emisión wildcard vía DNS-01 (ejemplo Cloudflare) |
| `scripts/vault-pki.sh` | CA interna con Vault PKI de HashiCorp |
| `scripts/cert-expiry-check.sh` | Revisa todos los secrets TLS de Kubernetes, avisa bajo N días |
| `scripts/ct-watch.sh` | Consulta logs CT de crt.sh por certificados inesperados |
| `scripts/ocsp-refresh.sh` | Recarga nginx para refrescar OCSP stapling tras renovación |
| `k8s/cert-manager.yaml` | Manifiestos ClusterIssuer (Let's Encrypt) + Certificate |
| `sql/inventory-dashboard.sql` | Consulta de inventario con buckets CRITICAL/WARNING/INFO |
| `nginx/tls-hardening.conf` | Solo TLS 1.2/1.3, política de ciphers, HSTS preload |

## Uso

Revisá cada script antes de ejecutar — rutas (`/var/www/certbot`), nombres de contenedores (`nginx`), dominios (`example.com`) y rutas de secretos son placeholders. Probá en staging primero.
