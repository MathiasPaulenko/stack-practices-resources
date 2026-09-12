# Golden Master Testing — Recursos Complementarios

Código complementario para el [Patrón Golden Master Testing](https://stackpractices.com/es/patterns/golden-master-testing-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `legacy_calculator.py` | Python 3.12+ | El sistema legacy que queremos refactorizar (sin tests, comportamiento poco claro) |
| `refactored_calculator.py` | Python 3.12+ | La versión refactorizada usando tabla de dispatch |
| `generate_golden_master.py` | Python 3.12+ | Genera 258 inputs de prueba, corre el sistema legacy, guarda el golden master |
| `test_golden_master.py` | Python 3.12+ + pytest 8.3 | Verifica que el código refactorizado coincide con el golden master (258 casos) |
| `test_inputs.json` | JSON | 3 inputs de muestra para pruebas rápidas |
| `golden_master.json` | JSON | 258 outputs capturados con hashes SHA-256 |
| `normalize_output.py` | Python 3.12+ | Normaliza valores no deterministas (timestamps, UUIDs, IDs) |

## Inicio rápido

### Generar el golden master (antes de refactorizar)

```bash
python generate_golden_master.py golden_master.json
# Output: Golden master generated with 258 cases -> golden_master.json
```

### Correr los tests del golden master (después de refactorizar)

```bash
python -m pytest test_golden_master.py -v
# Output: 258 passed
```

### Verificar un solo input

```bash
echo '{"operation":"add","a":1,"b":2}' | python legacy_calculator.py
echo '{"operation":"add","a":1,"b":2}' | python refactored_calculator.py
# Ambos deben producir output idéntico
```

## Cómo funciona

1. `generate_golden_master.py` crea 258 inputs diversos (casos normales, límite, frontera) y los corre por `legacy_calculator.py`.
2. Para cada input, captura el output y calcula un hash SHA-256.
3. Todos los inputs, outputs y hashes se guardan en `golden_master.json`.
4. `test_golden_master.py` corre los mismos inputs por `refactored_calculator.py` y compara los hashes.
5. Si los 258 hashes coinciden, el refactor preservó el comportamiento.

## Flujo de trabajo

```bash
# Paso 1: Generar golden master (antes de cualquier cambio)
python generate_golden_master.py

# Paso 2: Refactorizar legacy_calculator.py -> refactored_calculator.py

# Paso 3: Correr los tests del golden master
python -m pytest test_golden_master.py -v

# Paso 4: Si todos pasan, el refactor es seguro. Borra el golden master cuando tengas unit tests propios.
```
