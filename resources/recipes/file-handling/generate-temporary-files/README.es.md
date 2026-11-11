# Generar Archivos Temporales — código complementario

Versiones ejecutables de las cuatro implementaciones de la receta
[Generar Archivos Temporales](https://stackpractices.com/es/recipes/generate-temporary-files/)
de StackPractices. Cada una muestra las tres garantías que una API de
temporales debe dar: nombre impredecible, creación atómica y limpieza
determinista.

## Estructura

| Ruta | Qué muestra |
| --- | --- |
| `python/temp_files.py` | `NamedTemporaryFile`, `TemporaryDirectory`, `mkstemp`, `fsync` + `os.replace` atómico, `shutil.rmtree` recursivo |
| `node/temp_files.js` | `fs.mkdtemp`, nombres crypto-aleatorios con creación exclusiva `wx`, hooks de salida del paquete `tmp` |
| `java/TempFileExample.java` | `Files.createTempFile` / `createTempDirectory`, orden de registro de `deleteOnExit`, `Files.walk` en try-with-resources |
| `bash/temp_files.sh` | `mktemp` / `mktemp -d`, un solo `trap cleanup EXIT` que preserva el estado de salida real |

## Ejecutar

```bash
python python/temp_files.py

cd node && npm install && node temp_files.js

cd java && javac TempFileExample.java && java TempFileExample

bash bash/temp_files.sh
```

Sin build ni servicios: cada script limpia sus propios temporales al salir.
