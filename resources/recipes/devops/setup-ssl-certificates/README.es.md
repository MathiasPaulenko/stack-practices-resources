# Configurar certificados SSL con Let's Encrypt — Recursos complementarios

Archivos complementarios de [Configurar Certificados SSL con Let's Encrypt](https://stackpractices.com/es/recipes/setup-ssl-certificates/) en StackPractices.

## Archivos

| Archivo | Qué demuestra |
|---------|---------------|
| `docker-compose.yml` | nginx + sidecar de certbot con bucle de renovación (`certbot renew` cada 12h) |
| `nginx.conf` | Redirección HTTP→HTTPS con la ruta ACME `/.well-known/acme-challenge/` mapeada al volumen compartido |
| `cloudflare.ini.example` | Plantilla de credenciales para `certbot-dns-cloudflare` (certificados wildcard vía DNS-01) |
| `cert-manager.yaml` | `ClusterIssuer` + `Ingress` para certificados automáticos en Kubernetes |

## Cómo usarlo

Setup con Docker (sustituye `example.com` por tu dominio real):

```bash
mkdir -p certbot/conf certbot/www certbot/log
docker compose up -d
```

Emite el primer certificado:

```bash
docker compose run --rm certbot certonly --webroot \
  -w /var/www/certbot -d example.com -d www.example.com
```

Para Kubernetes, `kubectl apply -f cert-manager.yaml` tras instalar cert-manager.

El archivo de credenciales `cloudflare.ini` debe quedar en `chmod 600` — contiene un API token en texto plano.
