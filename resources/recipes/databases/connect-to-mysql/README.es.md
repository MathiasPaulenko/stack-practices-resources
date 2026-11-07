# Conectar a MySQL

Companion ejecutable de la receta [Conectar a MySQL](https://stackpractices.com/es/recipes/connect-to-mysql/): pool de conexiones, consultas parametrizadas, transacciones, reintentos con backoff e inserts por lotes en Python, JavaScript y Java.

## Contenido

- `docker-compose.yml` + `init.sql` — MySQL 8.4 local con datos de prueba
- `connect.py` — pool de `mysql-connector-python` + gestor de contexto + retry con `tenacity`
- `connect.js` — Pool de `mysql2` + transacción (`beginTransaction`/`commit`/`rollback`) + keepalive + `pool.end()`
- `MySQLPool.java` — pool HikariCP + consultas preparadas + insert por lotes
- `requirements.txt`, `package.json`

## Cómo ejecutarlo

```bash
docker compose up -d          # arranca MySQL en localhost:3306

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — necesita los jars mysql-connector-j + HikariCP en el classpath
javac -cp ".:mysql-connector-j.jar:HikariCP.jar" MySQLPool.java
java -cp ".:mysql-connector-j.jar:HikariCP.jar:slf4j-api.jar" MySQLPool
```

## Notas

- Las credenciales salen de variables de entorno (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) con valores por defecto para desarrollo local. Nunca escribas credenciales de producción en el código.
- El desarrollo local va sin SSL. En producción activa `ssl_ca` / `sslMode=VERIFY_CA` y apunta el driver a un bundle CA actual — en AWS RDS, la autenticación IAM de base de datos reemplaza las contraseñas guardadas.
- El timeout de inactividad del pool debe quedar por debajo del `wait_timeout` del servidor (28800s por defecto) o las conexiones inactivas vuelven muertas.
- Usa el charset `utf8mb4` — el `utf8` de MySQL solo tiene 3 bytes y corrompe en silencio los caracteres de 4 bytes.
