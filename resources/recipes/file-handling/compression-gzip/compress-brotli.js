// Brotli/Gzip streaming pipeline with content-negotiation middleware.
// Run: node compress-brotli.js

const zlib = require('zlib');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { pipeline } = require('stream');
const { promisify } = require('util');
const pipe = promisify(pipeline);

async function compressBrotli(srcPath, destPath, quality = 11) {
  const src = fs.createReadStream(srcPath);
  const brotli = zlib.createBrotliCompress({
    params: {
      [zlib.constants.BROTLI_PARAM_QUALITY]: quality,
      [zlib.constants.BROTLI_PARAM_MODE]: zlib.constants.BROTLI_MODE_TEXT,
    },
  });
  const dest = fs.createWriteStream(destPath);
  await pipe(src, brotli, dest);
}

async function compressGzip(srcPath, destPath, level = 6) {
  const src = fs.createReadStream(srcPath);
  const gzip = zlib.createGzip({ level });
  const dest = fs.createWriteStream(destPath);
  await pipe(src, gzip, dest);
}

// Express-style middleware: negotiate the best shared encoding.
// Attach with app.use(smartCompression()).
function smartCompression() {
  return (req, res, next) => {
    const acceptEncoding = req.headers['accept-encoding'] || '';
    const originalSend = res.send.bind(res);

    res.send = function (body) {
      if (typeof body === 'string' && body.length > 1024) {
        if (acceptEncoding.includes('br')) {
          res.setHeader('Content-Encoding', 'br');
          res.setHeader('Vary', 'Accept-Encoding');
          body = zlib.brotliCompressSync(body, {
            params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 4 },
          });
        } else if (acceptEncoding.includes('gzip')) {
          res.setHeader('Content-Encoding', 'gzip');
          res.setHeader('Vary', 'Accept-Encoding');
          body = zlib.gzipSync(body, { level: 6 });
        }
      }
      originalSend(body);
    };
    next();
  };
}

async function main() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'compress-'));
  const src = path.join(tmp, 'bundle.js');
  fs.writeFileSync(src, 'const x = () => console.log("hello world");\n'.repeat(4000));

  await compressGzip(src, src + '.gz', 9);
  await compressBrotli(src, src + '.br', 11);

  const size = fs.statSync(src).size;
  const gz = fs.statSync(src + '.gz').size;
  const br = fs.statSync(src + '.br').size;
  console.log(`Original: ${size} bytes`);
  console.log(`Gzip-9:   ${gz} bytes (${((gz / size) * 100).toFixed(1)}%)`);
  console.log(`Brotli-11:${br} bytes (${((br / size) * 100).toFixed(1)}%)`);
}

if (require.main === module) main();
module.exports = { smartCompression };
