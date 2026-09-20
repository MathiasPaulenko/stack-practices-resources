# Autenticación de Dos Factores (TOTP) — Recursos Companion

Companion ejecutable de la receta **[Autenticación de Dos Factores](https://stackpractices.com/es/recipes/two-factor-authentication/)** en StackPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `totp_service.py` | Servicio Python: `enroll()` → `confirm()` → `verify()` con almacenamiento de secretos encriptado (AES), códigos de respaldo hasheados de un solo uso y rate limit de 5 intentos por 5 minutos. |
| `totp-service.js` | Equivalente Node con `otplib` + encriptación AES-256-GCM vía `crypto`. Mismo contrato enroll → confirm → verify. |
| `test_totp.py` | Suite pytest que cubre los cuatro escenarios de la receta: round-trip de enrolamiento, borde de ventana, rate limiting y códigos de respaldo de un solo uso. |

## Inicio rápido — Python

```bash
pip install pyotp qrcode pillow cryptography pytest
export TOTP_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
pytest test_totp.py -v
```

```python
from totp_service import TOTPService

svc = TOTPService(issuer="MyApp")
out = svc.enroll("u_4812", "user@example.com")
# → muestra out["qr_png_b64"] como <img src="data:image/png;base64,...">
result = svc.confirm("u_4812", "123456")   # primer código de la app
if result["enabled"]:
    print(result["backup_codes"])          # mostrar UNA vez; el usuario los guarda

# en cada login:
ok = svc.verify("u_4812", "654321")
```

## Inicio rápido — Node

```bash
npm install otplib qrcode
export TOTP_ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
```

```javascript
const { TOTPService } = require('./totp-service');
const svc = new TOTPService('MyApp');

const { qrDataUrl } = await svc.enroll('u_4812', 'user@example.com');
// renderiza qrDataUrl en un <img> — el usuario lo escanea
const { enabled, backupCodes } = svc.confirm('u_4812', '123456');
// en el login:
const ok = svc.verify('u_4812', '654321');
```

## Notas

- **Nunca habilites al enrolar.** `confirm()` requiere un código válido antes de `enabled=true` — si no, un usuario que escanea mal se bloquea a sí mismo.
- **Clave de encriptación**: env var `TOTP_ENCRYPTION_KEY` (clave Fernet para Python, hex de 32 bytes para Node). En producción, obténla de KMS/Vault, no de un archivo.
- **Los códigos de respaldo son de un solo uso**: se almacenan como hashes SHA-256 y se queman al verificar. Muéstralos al usuario exactamente una vez.
- **El rate limit aquí es en memoria** por claridad — mueve el contador de intentos a Redis para despliegues multi-instancia (misma política de 5 por 5 min).
- La versión Python usa Fernet (AES-128-CBC + HMAC) por brevedad; la Node usa AES-256-GCM. Cualquiera sirve — lo que importa es que los secretos nunca estén en plaintext en reposo.
