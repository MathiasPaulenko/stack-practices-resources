# Feature Flags: Rollout, Segmentación y Rollback Seguro

Recurso companion de la [receta de Feature Flags](https://stackpractices.com/es/recipes/feature-flags/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `feature_flags.py` | Servicio de flags en Python con rollouts booleanos, porcentuales, por usuario y por grupo |
| `feature_flags.js` | Servicio de flags en JavaScript (ES module) |
| `FeatureFlags.java` | Servicio de flags en Java |
| `rollout_plan.py` | Plan de rollout escalonado para incrementar el porcentaje gradualmente |
| `ab_test.js` | Asignación de variantes A/B con bucketing determinístico |
| `launchdarkly_example.py` | Ejemplo de cliente managed con LaunchDarkly |
| `test_feature_flags.py` | Tests con pytest para el servicio de flags en Python |

## Inicio rápido

### Python

```bash
python feature_flags.py
```

### JavaScript

```bash
node feature_flags.js
```

### Java

```bash
javac FeatureFlags.java && java FeatureFlags
```

### Ejecutar tests

```bash
pip install pytest
pytest test_feature_flags.py -v
```

### Simulación de A/B test

```bash
node ab_test.js
```

### Simulación de rollout plan

```bash
python rollout_plan.py
```

### Ejemplo con LaunchDarkly

```bash
pip install ldclient
export LAUNCHDARKLY_SDK_KEY="your-sdk-key"
python launchdarkly_example.py
```

## Licencia

MIT
