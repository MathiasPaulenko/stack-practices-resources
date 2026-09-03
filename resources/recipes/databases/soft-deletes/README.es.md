# Companion de Soft Deletes

Implementaciones del patrón soft delete en Python, JavaScript y Java con tests.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_soft_deletes.py` | Python | SQLAlchemy SoftDeleteMixin, modelos User/Post, funciones restore y purge |
| `javascript_soft_deletes.js` | JavaScript | Sequelize paranoid models con restore y purge |
| `java_soft_deletes.java` | Java | JPA/Hibernate con @Filter para filtrado de soft delete |
| `sql_schema.sql` | SQL | Schema PostgreSQL con índices únicos parciales y tabla de auditoría |
| `test_soft_deletes.py` | Python | Tests pytest para visibilidad, restore, purge, cascade |
| `test_soft_deletes.js` | JavaScript | Tests Jest para visibilidad, restore, purge |

## Inicio Rápido

### Python

```bash
pip install -r requirements.txt
python python_soft_deletes.py
pytest test_soft_deletes.py -v
```

### JavaScript

```bash
npm install
node javascript_soft_deletes.js
npx jest test_soft_deletes.js
```

### PostgreSQL (Docker)

```bash
docker-compose up -d
psql -h localhost -U demo -d soft_deletes_demo -f sql_schema.sql
```

## Features Clave

- Columna `deleted_at` timestamp (NULL = activo)
- Columna `deleted_by` para auditoría de quién borró
- `query_visible()` / `paranoid: true` / `@Filter` para filtrado por defecto
- Índices únicos parciales (`WHERE deleted_at IS NULL`)
- Flujo de restauración (setear `deleted_at = NULL`)
- Purge job con ventana de retención
- Soft delete y restore en cascada para registros relacionados
- Métricas Prometheus para monitoreo
