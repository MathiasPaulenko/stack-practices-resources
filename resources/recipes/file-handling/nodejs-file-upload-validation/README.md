# Node.js File Upload Validation — Companion Resources

Runnable code referenced by
[Node.js File Upload Validation: Type, Size, and Content](https://stackpractices.com/recipes/nodejs-file-upload-validation/).

| File | Purpose |
| --- | --- |
| `upload.js` | Full Express pipeline: size/count limits, extension + MIME filter, `file-type` signature verification, error middleware |
| `avatar.js` | `memoryStorage` + Sharp: dimension limits, resize, EXIF strip via re-encode |

Both files are standalone apps — install `express multer@^2 file-type` (plus
`sharp` for `avatar.js`) and run with `node <file>.js`. Requires multer 2.x;
the deprecated 1.x line has known vulnerabilities.

Validation runs in layers — limits and filters first (cheap), content
verification last. Never trust a single check.
