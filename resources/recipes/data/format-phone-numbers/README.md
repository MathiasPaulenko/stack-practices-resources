# How to Format Phone Numbers (Python, JS, Java)

Runnable examples that parse, validate, and format international phone numbers with libphonenumber ports.
Companion code for the recipe at https://stackpractices.com/recipes/format-phone-numbers/

## Files

| File | Language | What it shows |
|---|---|---|
| `format_phone.py` | Python | `phonenumbers.parse`, validity flags, all output formats, extension and number type |
| `format-phone.js` | JavaScript | `parsePhoneNumberFromString`, `AsYouType` live formatting |
| `PhoneFormatter.java` | Java | `PhoneNumberUtil` parse/format, `AsYouTypeFormatter`, `getNumberType` |

## Run

```bash
# Python — pip install phonenumbers
python format_phone.py

# JavaScript — npm install libphonenumber-js
node format-phone.js

# Java — requires libphonenumber on the classpath (Maven: com.googlecode.libphonenumber:libphonenumber)
javac -cp libphonenumber.jar PhoneFormatter.java && java -cp .:libphonenumber.jar PhoneFormatter
```

Each example parses messy user input with a region hint, checks `possible` vs `valid`, and prints the
E.164, international, national, and RFC3966 (`tel:` URI) forms. The invalid sample shows the parse-error
path.
