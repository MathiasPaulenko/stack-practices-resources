# Ansible Playbook — Companion Files

Runnable companion for the [Ansible Playbook recipe](https://stackpractices.com/recipes/ansible-playbook/) on StackPractices.

- `inventory.ini` — host inventory with a `webservers` group.
- `site.yml` — playbook that installs Nginx, deploys a config template, and reloads the service via a handler.
- `ansible.cfg` — project-level settings pointing at the inventory.

Run it:

```bash
ansible-playbook site.yml --check --diff   # dry run
ansible-playbook site.yml                 # real run
```

Note: `site.yml` expects `templates/nginx.conf.j2` — create the template or swap the `template` task for a `copy` task with an inline `content:` block.
