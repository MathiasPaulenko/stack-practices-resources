# Hash de Contraseñas con Argon2

Código complementario de [Hash de Contraseñas con Argon2](https://stackpractices.com/es/recipes/hash-passwords-argon2/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `hash_argon2.py` | Hash Argon2id, verificación y rehash al actualizar parámetros en Python |
| `migrate_bcrypt.py` | Verificación híbrida que actualiza hashes bcrypt a Argon2id en el login |
| `hash_argon2.js` | Hash Argon2id, verificación y `needsRehash` en Node.js |
| `HashArgon2.java` | Argon2id con Bouncy Castle, comparación en tiempo constante con `MessageDigest.isEqual` |
| `pom.xml` | Dependencias Maven para el ejemplo Java |
| `requirements.txt` | Dependencias de Python |
| `package.json` | Dependencias de Node.js |

## Inicio rápido

### Python

```bash
pip install -r requirements.txt
python hash_argon2.py
python migrate_bcrypt.py
```

### JavaScript (Node.js)

```bash
npm install
npm run argon2
```

### Java

```bash
mvn compile exec:java -Dexec.mainClass=HashArgon2
```

Cada script imprime el string PHC generado, su tiempo de hashing en milisegundos
(objetivo: 250–500 ms en tu hardware) y los resultados de verificación válida e
inválida.
