# Generate URL Slugs — Companion Code

Runnable versions of the slug generators from the StackPractices recipe:
[How to Generate URL Slugs (Python, JS, Java)](https://stackpractices.com/recipes/generate-slugs/)

## Files

| File | Language | Notes |
| --- | --- | --- |
| `slug_generator.py` | Python 3 | stdlib only (`unicodedata` + `re`); includes uniqueness handling |
| `generate-slug.js` | Node.js 18+ | zero dependencies; basic + configurable variant |
| `SlugGenerator.java` | Java 11+ | JDK only (`Normalizer`); compile and run `main` |
| `slug.go` | Go 1.20+ | requires `golang.org/x/text` |

## Run

```bash
python slug_generator.py
node generate-slug.js
javac SlugGenerator.java && java SlugGenerator
go mod init slugdemo && go get golang.org/x/text && go run slug.go
```

Expected output for every implementation:

```text
hello-world-2024
cafe-creme-brulee
```
