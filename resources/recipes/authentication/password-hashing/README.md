# Password Hashing with bcrypt, Argon2 and PBKDF2

Companion code for [How to Hash Passwords Securely](https://stackpractices.com/recipes/password-hashing/).

## Files

| File | Description |
| --- | --- |
| `hash_bcrypt.py` | bcrypt hash and verify in Python |
| `hash_argon2.py` | Argon2id hash and verify in Python |
| `hash_pbkdf2.py` | PBKDF2-HMAC-SHA-256 hash and verify in Python |
| `hash_bcrypt.js` | bcrypt hash and verify in Node.js |
| `hash_argon2.js` | Argon2id hash and verify in Node.js |
| `hash_pbkdf2.js` | PBKDF2-HMAC-SHA-256 hash and verify in Node.js |
| `HashBcrypt.java` | bcrypt with `BCryptPasswordEncoder` |
| `HashArgon2.java` | Argon2id with `argon2-jvm` |
| `HashPBKDF2.java` | PBKDF2 with `javax.crypto` |
| `pom.xml` | Maven dependencies for the Java examples |
| `requirements.txt` | Python dependencies |
| `package.json` | Node.js dependencies |

## Quick start

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
# Compile
mvn compile

# Run each example
mvn exec:java -Dexec.mainClass=HashBcrypt
mvn exec:java -Dexec.mainClass=HashArgon2
mvn exec:java -Dexec.mainClass=HashPBKDF2
```

## Benchmarking the work factor

Each script prints the time it takes to hash `supersecret` on your machine. Tune
the cost/iteration/memory parameters until a single hash takes 100–250 ms on
your production hardware.
