# Infraestructura Inmutable — Companion

Código de acompañamiento para la receta de StackPractices [Infraestructura Inmutable](https://stackpractices.com/es/recipes/immutable-infrastructure/).

## Archivos

- `check_immutable.py` — checker estático (solo stdlib) que audita manifests de Docker Compose / Kubernetes buscando violaciones de inmutabilidad: tags `:latest`, digests no fijados, root filesystems escribibles, SSH expuesto, volúmenes `hostPath`, contenedores privilegiados.

## Uso

```bash
python check_immutable.py --demo              # corre contra un ejemplo con violaciones
python check_immutable.py deployment.yaml     # audita tus propios manifests
```

El exit code es `1` cuando hay violaciones, así puede bloquear un job de CI:

```yaml
- name: Enforce immutability
  run: python check_immutable.py k8s/*.yaml
```
