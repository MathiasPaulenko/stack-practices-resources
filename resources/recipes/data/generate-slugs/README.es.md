# Generar Slugs para URLs — Código complementario

Versiones ejecutables de los generadores de slugs de la receta de StackPractices:
[Cómo Generar Slugs para URLs (Python, JS, Java)](https://stackpractices.com/es/recipes/generate-slugs/)

## Archivos

| Archivo | Lenguaje | Notas |
| --- | --- | --- |
| `slug_generator.py` | Python 3 | solo stdlib (`unicodedata` + `re`); incluye manejo de unicidad |
| `generate-slug.js` | Node.js 18+ | cero dependencias; variante básica + configurable |
| `SlugGenerator.java` | Java 11+ | solo JDK (`Normalizer`); compilar y ejecutar `main` |
| `slug.go` | Go 1.20+ | requiere `golang.org/x/text` |

## Ejecutar

```bash
python slug_generator.py
node generate-slug.js
javac SlugGenerator.java && java SlugGenerator
go mod init slugdemo && go get golang.org/x/text && go run slug.go
```

Salida esperada en todas las implementaciones:

```text
hello-world-2024
cafe-creme-brulee
```
