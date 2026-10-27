# Playbook de Ansible — Archivos Complementarios

Proyecto ejecutable de la [receta de Playbook de Ansible](https://stackpractices.com/es/recipes/ansible-playbook/) en StackPractices.

- `inventory.ini` — inventario de hosts con un grupo `webservers`.
- `site.yml` — playbook que instala Nginx, despliega una plantilla de config y recarga el servicio vía un handler.
- `ansible.cfg` — configuración a nivel de proyecto apuntando al inventario.

Ejecútalo:

```bash
ansible-playbook site.yml --check --diff   # simulación
ansible-playbook site.yml                 # ejecución real
```

Nota: `site.yml` espera `templates/nginx.conf.j2` — crea la plantilla o cambia la tarea `template` por una tarea `copy` con un bloque `content:` inline.
