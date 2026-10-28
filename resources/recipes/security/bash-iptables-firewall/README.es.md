# Configurar Reglas de Firewall iptables con Bash

Scripts complementarios de la [receta de firewall iptables](https://stackpractices.com/es/recipes/bash-iptables-firewall/) en StackPractices.

Cada `.sh` es autocontenido: ajusta las variables de arriba y ejecútalo como root (o con sudo). Usan `set -euo pipefail` y ordenan las reglas de permitir antes que las políticas de descarte, para que un pegado línea a línea por SSH no te deje fuera.

## Requisitos

- Linux con iptables (o `iptables-nft` en distros basadas en nftables)
- Privilegios de root (`sudo` o shell de root)
- Debian/Ubuntu: `iptables-persistent` para `persist-rules.sh`; RHEL/Fedora: `iptables-services`
- Mantén **siempre** una segunda sesión SSH abierta mientras pruebas —una regla equivocada puede cortar tu propio acceso

## Scripts

| Archivo | Qué hace |
| --- | --- |
| `basic-firewall-setup.sh` | Ruleset base: loopback, ESTABLISHED, drop de INVALID, SSH/HTTP/HTTPS y políticas DROP |
| `ssh-rate-limit.sh` | Sustituye el ACCEPT plano de SSH por rate limiting con `-m recent` (máx 3 nuevas/min) |
| `nat-port-forwarding.sh` | Redirección DNAT + MASQUERADE/SNAT + FORWARD bidireccional |
| `block-ip-addresses.sh` | Inserta reglas DROP para una lista de IPs (antes de los permisos de puertos) |
| `allow-subnet-only.sh` | Restringe SSH a una subred |
| `persist-rules.sh` | `iptables-persistent`/`netfilter-persistent` + unit systemd restaurando v4 y v6 |
| `firewall-reset.sh` | Limpia todas las reglas y restaura políticas ACCEPT |
| `list-verify-rules.sh` | Vuelca las tablas filter/nat/mangle con contadores y números de línea |

## Licencia

MIT — igual que el repositorio stack-practices-resources.
