# Enviar Emails con SMTP — Recursos Companion

Envío de email SMTP listo para producción en Python, Node.js y Java con TLS, plantillas,
adjuntos y rate limiting.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `send_email.py` | Python | Clase `SmtpSender` con `smtplib`, plantillas, adjuntos, rate limiting |
| `send_email.js` | JavaScript | Clase `SmtpSender` con `nodemailer`, plantillas, rate limiting |
| `SmtpSender.java` | Java | Clase `SmtpSender` con Jakarta Mail, plantillas, adjuntos, rate limiting |
| `test_send_email.py` | Python | Tests unitarios para construcción de mensajes, plantillas, rate limiting |

## Requisitos

### Python

```bash
pip install pytest
```

### Node.js

```bash
npm install nodemailer
```

### Java

```bash
# Jakarta Mail (jakarta.mail-api 2.1 + eclipse-angus/mail)
# Maven:
#   <dependency>
#     <groupId>jakarta.mail</groupId>
#     <artifactId>jakarta.mail-api</artifactId>
#     <version>2.1.3</version>
#   </dependency>
#   <dependency>
#     <groupId>org.eclipse.angus</groupId>
#     <artifactId>jakarta.mail</artifactId>
#     <version>2.0.3</version>
#   </dependency>
```

## Ejecutar Tests

```bash
# Tests de Python
cd resources/recipes/api/send-emails-smtp
python -m pytest test_send_email.py -v
```

## Características

- TLS vía STARTTLS (puerto 587) o TLS implícito (puerto 465)
- Mensajes multipart de texto plano + HTML
- Adjuntos con detección automática de MIME type
- Sustitución de plantillas con variables de contexto
- Rate limiting para no exceder límites del proveedor
- Patrones de manejo de rebotes y reintentos

## Ver También

- [Receta completa](https://stackpractices.com/es/recipes/send-emails-smtp/)
- [Full recipe (EN)](https://stackpractices.com/recipes/send-emails-smtp/)
