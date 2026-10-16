# Reglas avanzadas de firewall con iptables

Scripts y configuraciones complementarios de la recipe de StackPractices
[Reglas avanzadas de firewall con iptables](https://stackpractices.com/es/recipes/bash-iptables-firewall-rules/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `firewall-basic.sh` | Conjunto base: denegación por defecto, SSH con rate limit, persistencia con `iptables-save` |
| `firewall-ipv6.sh` | La misma política para IPv6 (`ip6tables`), incluyendo ICMPv6 obligatorio |
| `ddos-mitigation.sh` | Límites con `connlimit`, rate limit de conexiones nuevas, SYNPROXY, ICMP limitado |
| `logging-setup.sh` | Target `LOG` con rate limit más ruteo por rsyslog a `/var/log/iptables.log` |
| `fail2ban/jail.local` | Jails de fail2ban para sshd, nginx-http-auth y reincidentes |
| `nftables.conf` | Conjunto equivalente en nftables (tabla `inet`, IPv4+IPv6 unificadas) |
| `knockd.conf` | Port knocking que abre/cierra SSH con una secuencia de golpes |

## Uso

Todos los scripts requieren root y asumen `iptables`/`ip6tables` instalados.

```bash
# Primero la base — aplícala con una sesión SSH verificada abierta
sudo bash firewall-basic.sh
sudo bash firewall-ipv6.sh

# Capas opcionales
sudo bash ddos-mitigation.sh
sudo bash logging-setup.sh

# fail2ban
sudo apt install fail2ban
sudo cp fail2ban/jail.local /etc/fail2ban/jail.local
sudo systemctl enable --now fail2ban

# Migración a nftables (reemplaza los scripts de iptables)
sudo nft -f nftables.conf
sudo systemctl enable --now nftables

# Port knocking
sudo apt install knockd
sudo cp knockd.conf /etc/knockd.conf
sudo systemctl enable --now knockd
```

**Advertencia:** la política de denegación por defecto aplica en el instante en que
corre `iptables -P INPUT DROP`. Aplica las reglas con una sesión verificada abierta,
o agenda un `iptables-restore` de un conjunto conocido-bueno como respaldo.
