# Guía Completa de Seguridad en LLMs - Ejemplos de Código

Capas de defensa ejecutables de la guía:
<https://stackpractices.com/es/guides/complete-guide-llm-security/>

## Instalación

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # solo necesario para red teaming en vivo
```

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `injection_guard.py` | Tripwire regex para formulaciones de inyección conocidas (señal, no veredicto) |
| `document_sanitizer.py` | Limpia portadores de instrucciones ocultas en docs recuperados |
| `jailbreak_detector.py` | Señal heurística de jailbreak (DAN, roleplay, autoridad, sondeo) |
| `output_filter.py` | Redacción de PII + código peligroso + política de URLs con dominio parseado |
| `rate_limiter.py` | Limitador de ventana deslizante por peticiones Y tokens (DoS de cartera) |
| `tool_validator.py` | Allowlist de herramientas + validación de argumentos + ámbito de sesión |
| `security_harness.py` | Corre el corpus estático de ataques por las capas |
| `attack_corpus.json` | Cadenas de ataque y benignas con resultados esperados |

## Verificación sin conexión

```bash
python security_harness.py --verbose
```

No requiere llamadas a la API - el corpus corre solo por las capas de
defensa. La clase `LLMRedTeam` de la guía extiende esto con ataques
generados contra un pipeline en vivo.
