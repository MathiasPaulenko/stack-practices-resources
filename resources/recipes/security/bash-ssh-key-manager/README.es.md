# Gestión de Llaves SSH en Bash — Recursos complementarios

Scripts ejecutables de la receta [Gestión de Llaves SSH en Bash](https://stackpractices.com/es/recipes/bash-ssh-key-manager/) de StackPractices.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `generate-key.sh` | Genera una llave ed25519 con permisos correctos en `~/.ssh`. |
| `distribute-key.sh` | Sube una llave pública a una lista de servidores (`ssh-copy-id` con fallback manual). |
| `rotate-key-verified.sh` | Rotación en flota que instala la llave nueva, verifica el login y recién después remueve la vieja. Segura de reejecutar. |
| `audit-keys-fleet.sh` | Audita `authorized_keys` en varios servidores y genera un CSV marcando llaves débiles (DSA, ECDSA, RSA < 4096). |
| `ssh-agent-ci.sh` | Setup no interactivo de `ssh-agent` para runners de CI; carga una llave en base64 desde `SSH_KEY`. |
| `sshd-hardening.sh` | Deshabilita la autenticación por password en `sshd_config` (valida con `sshd -t` antes de reiniciar). |
| `ssh-key-manager.py` | Wrapper de Python sobre `ssh-keygen` para inventario y auditoría de llaves débiles. |

## Uso

```bash
./generate-key.sh id_ed25519
./distribute-key.sh servers.txt
./rotate-key-verified.sh servers.txt
./audit-keys-fleet.sh web-01 web-02 db-01
python ssh-key-manager.py
```

`servers.txt` lleva un `user@host` por línea; los comentarios `#` y líneas vacías se ignoran.

Probalo primero en una VM descartable — estos scripts modifican `~/.ssh` y los `authorized_keys` remotos.
