# Comprimir y Descomprimir Archivos — Código complementario

Utilidades ejecutables de archivado para ZIP, GZIP y TAR en cuatro runtimes.
Fuente: <https://stackpractices.com/es/recipes/compress-decompress-files/>

## Archivos

| Archivo | Runtime | Qué hace |
| --- | --- | --- |
| `compress.py` | Python 3.9+ | Compresión ZIP en streaming, `decompress_zip_safe` con chequeos de zip-slip y zip-bomb, gzip por bloques, creación de tar.gz, listado de archivos |
| `compress.js` | Node.js 18+ | Pipelines de `zlib`, compresión de directorios con `archiver`, `extract-zip` con validación de rutas por componentes |
| `BatchCompressor.java` | JDK 11+ | Compresión batch con `java.util.zip` y `extractZipSafe` usando `Path.startsWith` |
| `compress.sh` | Bash | Creación de tar.gz, extracción segura, compresión paralela con `pigz`, gzip en masa |

## Uso

```bash
# Python (solo biblioteca estándar)
python compress.py zip logs/ logs.zip
python compress.py unzip upload.zip extracted/
python compress.py list archive.zip

# Node.js
npm install archiver extract-zip
node compress.js zip logs/ logs.zip
node compress.js unzip upload.zip extracted/

# Java
javac BatchCompressor.java

# Bash (carga las funciones)
source compress.sh
compress_tarball logs/ logs.tar.gz 6
extract_tarball_safe archive.tar.gz extracted/
```

## Seguridad en la extracción

Los tres extractores seguros comparan rutas resueltas componente a
componente, no como prefijos de texto, así que un miembro que resuelve a un
directorio hermano como `dest-evil/x` no puede pasar un chequeo pensado para
`dest/`. La versión Python también limita el tamaño total descomprimido
(`max_size`) para rechazar zip bombs.
