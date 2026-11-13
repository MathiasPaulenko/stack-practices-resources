# Helm Chart Review — `<Chart Name>`

## Review Overview

| Field | Value |
|-------|-------|
| Chart Name | example-app |
| Chart Version | 1.3.0 |
| App Version | 2.1.0 |
| Reviewer | DevOps Team |
| Review Date | 2026-07-05 |
| Kubernetes Version | 1.29+ |
| Helm Version | 3.14+ |

## 1. Chart Structure

| Check | Status | Notes |
|-------|--------|-------|
| Chart.yaml present and valid | ✅ | apiVersion: v2 |
| values.yaml present | ✅ | All defaults documented |
| templates/ directory exists | ✅ | 12 template files |
| _helpers.tpl present | ✅ | Named templates defined |
| .helmignore present | ✅ | Excludes .git, .vscode |
| README.md present | ✅ | Installation and configuration docs |
| values.schema.json present | ✅ | Type validation for all values |
| LICENSE present | ✅ | Apache 2.0 |
| charts/ directory (if dependencies) | ✅ | No subchart dependencies |
| NOTES.txt present | ✅ | Post-install instructions |

### Chart.yaml Validation

| Field | Value | Check |
|-------|-------|-------|
| apiVersion | v2 | ✅ Helm 3 format |
| name | example-app | ✅ Lowercase, no spaces |
| version | 1.3.0 | ✅ Semantic versioning |
| appVersion | 2.1.0 | ✅ Application version |
| description | Example web application | ✅ Descriptive |
| type | application | ✅ Application chart |
| keywords | [web, app, frontend] | ✅ Searchable |
| maintainers | [{name: devops-team, email: devops@example.com}] | ✅ Contact info |
| icon | https://example.com/icon.png | ✅ Chart icon |

## 2. Values Schema

### values.yaml Review

| Check | Status | Notes |
|-------|--------|-------|
| No secrets in values.yaml | ✅ | Secrets via --set or external secret store |
| All values have comments | ✅ | Every key documented |
| Sensible defaults | ✅ | Chart works with no overrides |
| No hardcoded environment values | ✅ | Environment-specific values overridden |
| Image tag uses appVersion | ✅ | `{{ .Chart.AppVersion }}` |
| Replica count defaults to > 1 | ✅ | Default: 3 |
| Resources have defaults | ✅ | requests and limits set |
| Service type is configurable | ✅ | Default: ClusterIP |

### values.schema.json Review

| Check | Status | Notes |
|-------|--------|-------|
| All values have type definitions | ✅ | String, integer, boolean, object |
| Required fields marked | ✅ | image.repository required |
| Enum values for restricted fields | ✅ | serviceType: [ClusterIP, NodePort, LoadBalancer] |
| Minimum/maximum for numeric fields | ✅ | replicas: min 1, max 100 |
| Pattern for string fields | ✅ | image.repository: non-empty string |
| Additional properties disabled | ✅ | additionalProperties: false |

### Values Structure

```yaml
replicaCount: 3

image:
  repository: ghcr.io/example/app
  pullPolicy: IfNotPresent
  tag: ""  # Overrides .Chart.AppVersion

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  automount: true
  annotations: {}
  name: ""

podAnnotations: {}
podLabels: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 10001
  runAsGroup: 10001
  fsGroup: 10001
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

autoscaling:
  enabled: false
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

volumes: []
volumeMounts: []

nodeSelector: {}
tolerations: []
affinity: {}

podDisruptionBudget:
  enabled: false
  minAvailable: 1

## 3. Template Review

| Check | Status | Notes |
|-------|--------|-------|
| No hardcoded namespaces | ☐ | Use .Release.Namespace |
| Labels follow conventions | ☐ | app.kubernetes.io/* labels |
| Selectors match labels | ☐ | Consistent across deployments and services |
| Named templates for repeated blocks | ☐ | _helpers.tpl for labels, names |
| No trailing whitespace | ☐ | {{- }} and {{- -}} used |
| Comments on complex logic | ☐ | Conditional blocks documented |
| No errors on empty values | ☐ | Defaults via `default` function |
| helm template renders cleanly | ☐ | `helm template . > /dev/null` |

## 4. Security Review

| Check | Status | Notes |
|-------|--------|-------|
| runAsNonRoot: true | ☐ | Pod and container level |
| readOnlyRootFilesystem: true | ☐ | Writable dirs via emptyDir |
| allowPrivilegeEscalation: false | ☐ | On every container |
| All capabilities dropped | ☐ | drop: [ALL] + specific adds |
| RBAC least privilege | ☐ | No cluster-admin, scoped rules |
| No secrets in values.yaml | ☐ | External store or --set |
| Image tag is not :latest | ☐ | Pinned tag or digest |
| seccompProfile set | ☐ | RuntimeDefault minimum |

## 5. Resource Management

| Check | Status | Notes |
|-------|--------|-------|
| CPU/memory requests set | ☐ | Every container |
| CPU/memory limits set | ☐ | Every container |
| HPA configurable | ☐ | autoscaling.enabled flag |
| PDB defined | ☐ | minAvailable or maxUnavailable |
| Priority class if needed | ☐ | For critical workloads |

## 6. Health Probes

| Check | Status | Notes |
|-------|--------|-------|
| livenessProbe defined | ☐ | Correct path/port/initialDelay |
| readinessProbe defined | ☐ | Gates traffic, not restarts |
| startupProbe for slow starters | ☐ | Avoids premature kills |
| Probe endpoints exist | ☐ | App actually serves them |

## 7. Deployment Strategy

| Check | Status | Notes |
|-------|--------|-------|
| strategy.type chosen deliberately | ☐ | RollingUpdate vs Recreate |
| maxSurge / maxUnavailable set | ☐ | Matches availability needs |
| revisionHistoryLimit reasonable | ☐ | Default 10 is usually too many |
| Rollback tested | ☐ | `helm rollback` verified in staging |

## 8. Testing

| Check | Status | Notes |
|-------|--------|-------|
| helm lint passes | ☐ | In CI on every PR |
| kube-score clean | ☐ | On rendered manifests |
| tests/ directory has test pods | ☐ | `helm test` works |
| Dry-run upgrade tested | ☐ | `helm upgrade --dry-run` |

## Sign-off

| Field | Value |
|-------|-------|
| Reviewed by | |
| Approved for | dev / staging / prod |
| Follow-up tickets | |
