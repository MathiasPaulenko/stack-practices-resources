# Templates de Email con MJML — Recursos Companion

Ejemplos ejecutables para la receta [Templates de Email Responsivos con MJML](https://stackpractices.com/es/recipes/email-templates-mjml/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `welcome.mjml` | Template básico de bienvenida con variables de Handlebars |
| `EmailRenderer.ts` | Pipeline de compilación MJML + renderizado Handlebars |
| `EmailSender.ts` | Sender SMTP con Nodemailer y multipart/alternative |
| `Button.mjml` | Componente de botón reutilizable para `mj-include` |
| `dark-mode.mjml` | Template con dark mode y media query `prefers-color-scheme` |
| `package.json` | Dependencias: mjml, handlebars, nodemailer, typescript |
| `tsconfig.json` | Configuración TypeScript strict |

## Inicio Rápido

```bash
npm install
npm run build

# Configurar variables SMTP
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
export SMTP_USER=your@gmail.com
export SMTP_PASS=your-app-password

# Enviar un correo de prueba
npm run send
```

## Testing Sin SMTP

Usa [Ethereal](https://ethereal.email/) para testing local:

```typescript
const transporter = nodemailer.createTransport({
  host: 'smtp.ethereal.email',
  port: 587,
  auth: {
    user: 'test@ethereal.email',
    pass: 'generated-password',
  },
});
```

## Puntos Clave

- Siempre envía `multipart/alternative` con HTML y texto plano.
- Mantén el ancho bajo 600px y el tamaño bajo 102KB.
- Prueba en Gmail, Outlook y Apple Mail antes de enviar.
- Escapa el input del usuario con el HTML escaping por defecto de Handlebars.
- Usa fuentes del sistema (Arial, Georgia, Verdana); las web fonts fallan en la mayoría de clientes.
