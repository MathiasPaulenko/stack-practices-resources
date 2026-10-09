// Archive utilities for Node.js: streaming pipelines and safe extraction.
// Requires Node.js 18+ and `npm install archiver extract-zip` (zlib is built in).

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const { pipeline } = require('stream');
const { promisify } = require('util');
const pipe = promisify(pipeline);

async function gzipFile(srcPath, destPath, level = 6) {
  const src = fs.createReadStream(srcPath);
  const gzip = zlib.createGzip({ level });
  const dest = fs.createWriteStream(destPath);
  await pipe(src, gzip, dest);
}

async function gunzipFile(srcPath, destPath) {
  const src = fs.createReadStream(srcPath);
  const gunzip = zlib.createGunzip();
  const dest = fs.createWriteStream(destPath);
  await pipe(src, gunzip, dest);
}

async function gzipDirectory(srcDir, destZip) {
  const archiver = require('archiver');
  const output = fs.createWriteStream(destZip);
  const archive = archiver('zip', { zlib: { level: 6 } });

  const done = new Promise((resolve, reject) => {
    output.on('close', () => resolve(archive.pointer()));
    output.on('error', reject);
    archive.on('error', reject);
  });

  archive.pipe(output);
  archive.directory(srcDir, false);
  archive.finalize();

  return await done;
}

async function extractZipSafe(zipPath, destDir) {
  const extract = require('extract-zip');
  const destRoot = path.resolve(destDir);

  await extract(zipPath, {
    dir: destRoot,
    onEntry: (entry) => {
      const rel = path.relative(destRoot, path.resolve(destRoot, entry.fileName));
      if (rel.startsWith('..') || path.isAbsolute(rel)) {
        throw new Error(`Unsafe path in archive: ${entry.fileName}`);
      }
    },
  });
}

module.exports = { gzipFile, gunzipFile, gzipDirectory, extractZipSafe };

// CLI usage: node compress.js <gzip|gunzip|zip|unzip> <src> [dest]
if (require.main === module) {
  const [cmd, src, dest = 'out'] = process.argv.slice(2);
  const fn = { gzip: gzipFile, gunzip: gunzipFile, zip: gzipDirectory, unzip: extractZipSafe }[cmd];
  if (!fn || !src) {
    console.log('Usage: node compress.js <gzip|gunzip|zip|unzip> <src> [dest]');
    process.exit(1);
  }
  fn(src, dest).then((r) => r != null && console.log(`Bytes: ${r}`))
    .catch((e) => { console.error(e.message); process.exit(1); });
}
