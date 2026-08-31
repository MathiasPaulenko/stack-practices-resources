# Hashing de Contraseñas con bcrypt, Argon2 y PBKDF2

Código complementario para [Cómo hashear contraseñas](https://stackpractices.com/es/recipes/password-hashing/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `hash_bcrypt.py` | Hash y verificación con bcrypt en Python |
| `hash_argon2.py` | Hash y verificación con Argon2id en Python |
| `hash_pbkdf2.py` | Hash y verificación con PBKDF2-HMAC-SHA-256 en Python |
| `hash_bcrypt.js` | Hash y verificación con bcrypt en Node.js |
| `hash_argon2.js` | Hash y verificación con Argon2id en Node.js |
| `hash_pbkdf2.js` | Hash y verificación con PBKDF2-HMAC-SHA-256 en Node.js |
| `HashBcrypt.java` | bcrypt con `BCryptPasswordEncoder` |
| `HashArgon2.java` | Argon2id con `argon2-jvm` |
| `HashPBKDF2.java` | PBKDF2 con `javax.crypto` |
| `pom.xml` | Dependencias Maven para los ejemplos Java |
| `requirements.txt` | Dependencias de Python |
| `package.json` | Dependencias de Node.js |

## Inicio rápido

### Python

```bash
pip install -r requirements.txt
python hash_bcrypt.py
python hash_argon2.py
python hash_pbkdf2.py
```

### JavaScript (Node.js)

```bash
npm install
npm run bcrypt
npm run argon2
npm run pbkdf2
```

### Java

```bash
# Compilar
mvn compile

# Ejecutar cada ejemplo
mvn exec:java -Dexec.mainClass=HashBcrypt
mvn exec:java -Dexec.mainClass=HashArgon2
mvn exec:java -Dexec.mainClass=HashPBKDF2
```

## Benchmark del factor de trabajo

Cada script imprime el tiempo que tarda en hashear `supersecret` en tu máquina.
Ajustá los parámetros de costo, iteraciones y memoria hasta que un solo hash
tarde 100–250 ms en tu hardware de producción.
