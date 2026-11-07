# Gzip & Brotli Compression — Companion Resources

Runnable examples for the [Compress and Decompress Files with Gzip and Brotli](https://stackpractices.com/recipes/compression-gzip/) recipe on StackPractices.

## Files

| File | What it shows |
|---|---|
| `gzip_streaming.py` | Streaming Gzip compress/decompress with SHA256 integrity check |
| `compress-brotli.js` | Node.js Brotli/Gzip pipelines + `smartCompression()` content-negotiation middleware |
| `precompress.sh` | Bash pre-compression of static assets (`.gz` + `.br`) for Nginx |
| `ratio_benchmark.py` | Compression-ratio benchmark: JSON/HTML/logs vs random vs tiny payloads |

## Run

```bash
python gzip_streaming.py      # compress + restore + SHA256 verify
node compress-brotli.js       # gz + br pipeline output with ratios
python ratio_benchmark.py     # why thresholds matter (random bytes grow!)
./precompress.sh dist/        # emits file.gz + file.br next to each asset
```

## Notes

- `smartCompression()` is Express middleware — it negotiates `br`/`gzip` from `Accept-Encoding` and sets `Vary: Accept-Encoding` so caches keep variants separate.
- `ratio_benchmark.py` makes the threshold case concrete: payloads under ~1KB and already-random data get *bigger* when compressed.
- Brotli needs `pip install brotli` for the Python benchmark; Node ≥11.7 ships `zlib.createBrotliCompress` built in.

Source article (EN): <https://stackpractices.com/recipes/compression-gzip/>
