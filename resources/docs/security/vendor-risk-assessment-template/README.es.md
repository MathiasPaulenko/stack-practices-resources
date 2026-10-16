# Plantilla de Evaluación de Riesgos de Proveedores — Archivos complementarios

Recursos complementarios del artículo
[Plantilla de Evaluación de Riesgos de Proveedores](https://stackpractices.com/es/docs/vendor-risk-assessment-template/)
en StackPractices.

## Contenido

- `assessment-workbook.md` — la plantilla de evaluación completa, lista para copiar.
- `vendor_security_check.py` — comprobaciones de postura pública del dominio de un proveedor (DNSSEC, nota TLS de SSL Labs, `security.txt`, historial de brechas en HIBP).
- `vendor_risk_scorer.py` — puntuación de riesgo ponderada y bandas de decisión según el libro de evaluación.
- `vendor_monitor.py` — lee `vendor-registry.yaml` y ejecuta las comprobaciones de cada proveedor.
- `vendor-monitoring.yml` — workflow de GitHub Actions que corre el monitor semanalmente.
- `vendor-registry.yaml` — formato del registro de proveedores para el monitor.

## Uso

```bash
pip install requests pyyaml

# Puntuar una evaluación completada
python vendor_risk_scorer.py

# Comprobar la postura pública de un proveedor
python vendor_security_check.py

# Monitorizar todo el registro (falla si un proveedor de alto riesgo degrada)
HIBP_API_KEY=<clave> python vendor_monitor.py --config vendor-registry.yaml
```

La API de SSL Labs es asíncrona — la primera llamada devuelve un estado (`IN_PROGRESS`) en vez de la nota; consulta `analyze?host=<dominio>&all=done` hasta que `status == "READY"`. El endpoint `/breacheddomain` de HIBP requiere una API key de pago en `HIBP_API_KEY`; sin ella esa comprobación se omite.

## Licencia

Libre para usar y adaptar bajo MIT. La atribución es bienvenida, no obligatoria.
