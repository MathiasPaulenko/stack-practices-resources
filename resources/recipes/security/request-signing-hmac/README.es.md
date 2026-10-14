# Firma de peticiones HMAC — Archivos complementarios

Código ejecutable de firma/verificación para la receta
[Firma HMAC para autenticación de API (AWS Sig v4)](https://stackpractices.com/es/recipes/request-signing-hmac/):
pares firma/verificación por lenguaje, un firmante AWS Signature v4
completo, un verificador de webhooks con protección anti-replay por
nonce y rotación de claves con solapamiento.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `sign_request.py` | Par firma/verificación en Python con `hmac.compare_digest`. Corre una demo de ida y vuelta autocontenida. |
| `sign-request.js` | Par firma/verificación en Node.js. El verificador protege `crypto.timingSafeEqual` con un chequeo de longitud (lanza excepción si difieren). |
| `RequestSigner.java` | Firmante Java que devuelve ambos headers — el timestamp tiene que viajar con la petición para que la verificación funcione. Incluye `main()` de demo. |
| `sign-request.go` | `SignRequest`/`VerifyRequest` en Go con chequeo de frescura de 5 minutos y `hmac.Equal`. |
| `aws-sigv4.py` | Firmante AWS Signature v4 completo: petición canónica, query normalizado y ordenado, cadena de derivación de clave, header `Authorization`. |
| `webhook-verify.js` | Verificador de webhooks en Express: ventana de frescura de timestamp + unicidad de nonce con `SET NX` en Redis + chequeo HMAC. |
| `key-rotation.py` | Dataclass `KeyRotation` — el secreto viejo y el nuevo verifican durante una hora de solapamiento. |

## Ejecutar

```bash
python sign_request.py       # ida y vuelta firma + verificación
python aws-sigv4.py          # imprime un header Authorization SigV4
python key-rotation.py       # muestra ambas claves válidas en el solapamiento
node sign-request.js         # ida y vuelta en JS
go run sign-request.go       # compila el par en Go

# El verificador de webhook necesita express + redis
npm install express redis && REDIS_URL=redis://localhost:6379 node webhook-verify.js

# Java
javac RequestSigner.java && java RequestSigner
```

## Notas

- `timingSafeEqual`/`hmac.Equal`/`compare_digest` son de tiempo
  constante — pero lanzan excepción cuando los largos difieren, así que
  el chequeo de longitud va primero siempre.
- Firmá el body crudo de la petición, no JSON re-serializado — el orden
  de claves y los espacios cambian los bytes y rompen la firma.
- El almacén de nonces es lo que realmente frena el replay dentro de la
  ventana de timestamp; sin eso una petición capturada se repite hasta
  quedar vieja.
- Preferí el firmante del SDK de AWS/`botocore` sobre `aws-sigv4.py` en
  producción — el archivo existe para tests de interoperabilidad y para
  entender la spec.
