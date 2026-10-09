# Compress and Decompress Files — Companion Code

Runnable archive utilities covering ZIP, GZIP, and TAR in four runtimes.
Source: <https://stackpractices.com/recipes/compress-decompress-files/>

## Files

| File | Runtime | What it does |
| --- | --- | --- |
| `compress.py` | Python 3.9+ | Streaming ZIP compression, `decompress_zip_safe` with zip-slip + zip-bomb checks, gzip chunking, tar.gz creation, archive listing |
| `compress.js` | Node.js 18+ | `zlib` pipelines, `archiver` directory compression, `extract-zip` with component-wise path validation |
| `BatchCompressor.java` | JDK 11+ | `java.util.zip` batch compression and `extractZipSafe` using `Path.startsWith` |
| `compress.sh` | Bash | tar.gz creation, safe extraction, `pigz` parallel compression, batch gzip |

## Usage

```bash
# Python (stdlib only)
python compress.py zip logs/ logs.zip
python compress.py unzip upload.zip extracted/
python compress.py list archive.zip

# Node.js
npm install archiver extract-zip
node compress.js zip logs/ logs.zip
node compress.js unzip upload.zip extracted/

# Java
javac BatchCompressor.java

# Bash (source the functions)
source compress.sh
compress_tarball logs/ logs.tar.gz 6
extract_tarball_safe archive.tar.gz extracted/
```

## Extraction safety

All three safe extractors compare resolved paths component-wise, not as
string prefixes, so a member resolving to a sibling directory like
`dest-evil/x` cannot pass a check meant for `dest/`. The Python version also
caps total uncompressed size (`max_size`) to reject zip bombs.
