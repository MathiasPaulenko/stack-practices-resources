# Estrategia de Branching Git: `<Proyecto/Equipo>`

> Versión: ______ | Última actualización: ______ | Responsable: ______

---

## 1. Tipos de Ramas

### Ramas Principales

| Rama | Propósito | Protección | Duración |
|------|-----------|------------|----------|
| `main` | Código listo para producción | Requiere PR + 2 aprobaciones + CI verde | Permanente |
| `staging` | Validación pre-producción | Requiere PR + 1 aprobación + CI verde | Permanente |
| `develop` | Rama de integración para features | Requiere PR + 1 aprobación + CI verde | Permanente |

### Ramas de Soporte

| Prefijo | Propósito | Fuente | Merge Target | Nomenclatura |
|---------|-----------|--------|--------------|--------------|
| `feature/` | Nueva funcionalidad | `develop` | `develop` | `feature/TICKET-descripcion-corta` |
| `bugfix/` | Fixes no urgentes | `develop` | `develop` | `bugfix/TICKET-descripcion-corta` |
| `hotfix/` | Fixes críticos de producción | `main` | `main` + `develop` | `hotfix/TICKET-descripcion-corta` |
| `release/` | Preparación de release | `develop` | `main` + `staging` | `release/v1.2.3` |
| `chore/` | Mantenimiento, dependencias | `develop` | `develop` | `chore/TICKET-descripcion-corta` |
| `docs/` | Solo documentación | `develop` | `develop` | `docs/TICKET-descripcion-corta` |

---

## 2. Flujo de Trabajo

### Desarrollo de Features

```bash
git checkout develop
git pull origin develop

## 2. Crear la rama de feature
git checkout -b feature/PROJ-123-add-user-auth

## 3. Trabajar y commitear en local
git commit -m "feat: add OAuth2 login endpoint"
git commit -m "test: add auth integration tests"

## 4. Push y abrir PR cuando esté listo
git push origin feature/PROJ-123-add-user-auth
## Abrir PR a develop, completar la plantilla

## 5. Tras aprobación y CI verde, mergear
git checkout develop
git merge --no-ff feature/PROJ-123-add-user-auth
## O usar squash merge desde la UI de GitHub/GitLab
```

### Flujo de Hotfix

```bash
## 1. Salir desde main
git checkout main
git pull origin main

## 2. Crear la rama de hotfix
git checkout -b hotfix/PROJ-456-fix-payment-webhook

## 3. Fix, test, commit
git commit -m "fix: validate webhook signature before processing"

## 4. Abrir PR a main (revisión expeditada)
git push origin hotfix/PROJ-456-fix-payment-webhook
## Pedir revisión de emergencia; target: main

## 5. Tras el merge a main, hacer backport a develop
git checkout develop
git cherry-pick <hotfix-commit>
## O mergear main en develop
```

### Flujo de Release

```bash
## 1. Crear rama de release desde develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.3

## 2. Bump de versión, actualizar changelog, QA final
git commit -m "chore: bump version to 1.2.3"

## 3. Mergear a staging para la validación final
git checkout staging
git merge --no-ff release/v1.2.3

## 4. Tras validar en staging, mergear a main
git checkout main
git merge --no-ff release/v1.2.3

## 5. Taggear el release
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3

## 6. Mergear de vuelta a develop para capturar los commits del release
git checkout develop
git merge --no-ff main
```

---

## 3. Convenciones de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[scope opcional]: <descripción>

[cuerpo opcional]

[footer(s) opcional(es)]
```

### Tipos

| Tipo | Uso Para | Dispara Release |
|------|----------|-----------------|
| `feat` | Nueva funcionalidad | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Solo documentación | Ninguno |
| `style` | Formateo, punto y coma faltante | Ninguno |
| `refactor` | Cambio sin cambio de comportamiento | Ninguno |
| `perf` | Mejora de rendimiento | Patch |
| `test` | Agregar o corregir tests | Ninguno |
| `chore` | Proceso de build, dependencias | Ninguno |
| `ci` | Cambios de CI/CD | Ninguno |
| `revert` | Revertir commit previo | Patch |

### Ejemplos

```
feat(auth): add Google OAuth2 login

Implements OAuth2 flow with PKCE for web clients.
Closes PROJ-123

fix(payments): validate webhook signature

Prevents replay attacks by verifying Stripe signature
header before processing events.

Closes PROJ-456
```

---

## 4. Requisitos de Merge

### Requisitos de Pull Request

| Requisito | Feature/Bugfix | Hotfix | Release |
|-----------|----------------|--------|---------|
| CI pasa | Requerido | Requerido | Requerido |
| Aprobaciones de review | 2 | 1 (expeditado) | 2 |
| Ticket enlazado | Requerido | Requerido | Requerido |
| Tests agregados | Requerido | Requerido | N/A |
| Documentación actualizada | Si cambia funcionalidad | Si cambia comportamiento | Changelog actualizado |
| Revisión de seguridad | Si auth/datos | Requerido | N/A |

### Estrategias de Merge

| Rama Target | Estrategia | Razonamiento |
|-------------|------------|--------------|
| `develop` | Squash and merge | Historial limpio; un commit por feature |
| `main` | Merge commit | Preserva el historial del release |
| `hotfix` a `main` | Merge commit | Preserva la identificación del hotfix |

---

## 5. Tagging y Versionado

Seguimos [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios breaking en API
- **MINOR**: Nuevas capacidades, retrocompatible
- **PATCH**: Bug fixes, retrocompatible

### Formato de Tag

```bash
## Releases de producción
git tag -a v1.2.3 -m "Release v1.2.3"

## Pre-releases
git tag -a v1.2.3-rc.1 -m "Release candidate 1"

## Hotfixes
git tag -a v1.2.4 -m "Hotfix: fix payment webhook validation"
```

### Reglas de Bump de Versión

| Tipo de Commit | Bump de Versión |
|----------------|-----------------|
| `feat` | Minor (x.Y.z) |
| `fix`, `perf`, `revert` | Patch (x.y.Z) |
| `feat` con `BREAKING CHANGE` | Major (X.y.z) |
| `docs`, `style`, `refactor`, `test`, `chore`, `ci` | Ninguno |

---

## 6. Procedimientos de Rollback

### Revertir un Despliegue

Prefiere `git revert` cuando el release malo ya está en main: agrega un commit nuevo en lugar de mover el historial. Hacer checkout a un tag anterior sirve para redesplegar un build bueno conocido, pero deja el HEAD detached.

```bash
## Identificar el último tag bueno conocido
git log --oneline --decorate --tags

## Volver al tag anterior
git checkout v1.2.2

## Crear rama de hotfix para el rollback
git checkout -b hotfix/rollback-v1.2.3

## Desplegar el rollback
git push origin hotfix/rollback-v1.2.3
## Abrir PR de emergencia a main
```

### Revertir un Merge

```bash
## Encontrar el commit de merge
git log --oneline --merges

## Revertir el merge (crea un nuevo commit de revert)
git revert -m 1 <merge-commit-hash>

## Abrir PR con el commit de revert
```

---

## 7. Reglas de Protección

### Branch Protection (GitHub/GitLab)

| Regla | main | staging | develop |
|-------|------|---------|---------|
| Requerir PR | Sí | Sí | Sí |
| Aprobaciones requeridas | 2 | 1 | 1 |
| Desechar aprobaciones stale | Sí | Sí | No |
| Requerir status checks | Sí | Sí | Sí |
| Incluir administradores | Sí | Sí | No |
| Requerir historial lineal | No | No | Sí |
| Permitir force push | No | No | No |
| Permitir borrados | No | No | No |