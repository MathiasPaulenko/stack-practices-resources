# Validación de Input — Recursos Complementarios

Ejemplos ejecutables de la [receta de validación de input](https://stackpractices.com/es/recipes/input-validation/) en StackPractices.

Validación schema-first: declara la forma una vez, deja que la librería rechace input malformado en el límite y devuelve errores por campo que el cliente puede mostrar junto a cada input.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `validate_user.py` | Modelo Pydantic v2 con restricciones `Field`, `field_validator`, `EmailStr` y un helper `format_errors()` que convierte `ValidationError` en un payload listo para un 400 |
| `test_validate_user.py` | Suite pytest: camino válido, rechazo de nombre vacío, límites de email/edad, agregación de errores |
| `validate_user.js` | Schema Zod con `safeParse` y un wrapper `validateUser()` que devuelve `{ data }` o `{ errors }` |
| `validate_user.test.js` | Suite `node:test` espejo de los tests de Python |

## Ejecutar

```bash
# Python (requiere pydantic[email] + pytest)
pip install -r requirements.txt
python validate_user.py
python -m pytest test_validate_user.py -v

# JavaScript (Node 18+)
npm install
node validate_user.js
node --test validate_user.test.js
```

## Ideas clave

- Valida en el límite; la capa de servicio debe recibir objetos tipados, no strings crudos.
- `safeParse` / `ValidationError` agregan *todas* las violaciones — el usuario corrige tres campos en un solo intento.
- La coerción es explícita: `"36"` se convierte en `36` solo donde el schema lo permite.
- Validación no es sanitización — escapa la salida según el contexto y parametriza las consultas por separado.

CI: `.github/workflows/test.yml` ejecuta ambas suites en cada cambio de esta carpeta.
