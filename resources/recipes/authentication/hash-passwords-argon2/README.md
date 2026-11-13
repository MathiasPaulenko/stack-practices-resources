# Hash Passwords with Argon2

Companion code for [Hash Passwords with Argon2](https://stackpractices.com/recipes/hash-passwords-argon2/).

## Files

| File | Description |
| --- | --- |
| `hash_argon2.py` | Argon2id hash, verify and rehash-on-upgrade in Python |
| `migrate_bcrypt.py` | Hybrid verification that upgrades bcrypt hashes to Argon2id on login |
| `hash_argon2.js` | Argon2id hash, verify and `needsRehash` in Node.js |
| `HashArgon2.java` | Argon2id with Bouncy Castle, constant-time `MessageDigest.isEqual` comparison |
| `pom.xml` | Maven dependencies for the Java example |
| `requirements.txt` | Python dependencies |
| `package.json` | Node.js dependencies |

## Quick start

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

Each script prints the generated PHC string, its hashing time in milliseconds
(target: 250–500 ms on your hardware), and valid/invalid verification results.
