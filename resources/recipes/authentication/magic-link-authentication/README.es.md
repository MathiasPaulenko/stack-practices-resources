# Autenticación con Magic Links — Express + Nodemailer

Companion ejecutable de
[Implementar Login Sin Contraseña con Magic Links](https://stackpractices.com/es/recipes/magic-link-authentication/).

Flujo de login sin contraseña: solicita un link por email, recibe un token
firmado de uso único (expira en 15 min, se guarda el hash — nunca el token
crudo), verifica vía POST para que el prefetch de scanners no lo consuma.

## Ejecutar

```bash
npm install
cp .env.example .env   # define APP_SECRET
npm start
```

Sin variables SMTP el servidor usa una cuenta de prueba Ethereal e imprime
la URL de preview del email enviado.

## Probar

```bash
# 1. Pide un link (respuesta uniforme en ambos casos)
curl -X POST http://localhost:3000/auth/login \
  -H 'content-type: application/json' -d '{"email":"tu@example.com"}'

# 2. Abre la URL de preview de Ethereal de la consola y copia el link.

# 3. Haz GET al link — muestra un formulario de confirmación (el token
#    aún no se consume). Envía el POST para consumirlo y obtener sesión.
curl -X POST http://localhost:3000/auth/verify -d 'token=<token>'

# 4. Comprueba la sesión
curl http://localhost:3000/auth/me -H 'x-session-id: <sessionId>'

# 5. Reutiliza el mismo link -> 400 "already used"
curl -X POST http://localhost:3000/auth/verify -d 'token=<token>'
```
