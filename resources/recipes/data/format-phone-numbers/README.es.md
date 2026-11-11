# Cómo Formatear Números de Teléfono (Python, JS, Java)

Ejemplos ejecutables que parsean, validan y formatean números de teléfono internacionales con ports de
libphonenumber. Código complementario de la receta en https://stackpractices.com/es/recipes/format-phone-numbers/

## Archivos

| Archivo | Lenguaje | Qué muestra |
|---|---|---|
| `format_phone.py` | Python | `phonenumbers.parse`, flags de validez, todos los formatos de salida, extensión y tipo de número |
| `format-phone.js` | JavaScript | `parsePhoneNumberFromString`, formateo en vivo con `AsYouType` |
| `PhoneFormatter.java` | Java | Parseo/formateo con `PhoneNumberUtil`, `AsYouTypeFormatter`, `getNumberType` |

## Ejecutar

```bash
# Python — pip install phonenumbers
python format_phone.py

# JavaScript — npm install libphonenumber-js
node format-phone.js

# Java — requiere libphonenumber en el classpath (Maven: com.googlecode.libphonenumber:libphonenumber)
javac -cp libphonenumber.jar PhoneFormatter.java && java -cp .:libphonenumber.jar PhoneFormatter
```

Cada ejemplo parsea input desprolijo de usuario con un hint de región, chequea `possible` vs `valid`, e
imprime las formas E.164, internacional, nacional y RFC3966 (URI `tel:`). El ejemplo inválido muestra el
camino de error de parseo.
