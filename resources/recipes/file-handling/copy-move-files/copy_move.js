// Copy and move files with fs.promises, checksums, and cross-device fallback.
const fs = require('fs').promises;
const crypto = require('crypto');

async function sha256(file) {
  const data = await fs.readFile(file);
  return crypto.createHash('sha256').update(data).digest('hex');
}

async function copyWithChecksum(src, dest) {
  await fs.copyFile(src, dest, fs.constants.COPYFILE_FICLONE);
  if (await sha256(src) !== await sha256(dest)) {
    await fs.unlink(dest);
    throw new Error(`Checksum mismatch: ${src} -> ${dest}`);
  }
}

async function moveWithFallback(src, dest) {
  try {
    await fs.rename(src, dest);
  } catch (err) {
    if (err.code === 'EXDEV') {
      const stat = await fs.stat(src);
      if (stat.isDirectory()) {
        await fs.cp(src, dest, { recursive: true });
        await fs.rm(src, { recursive: true });
      } else {
        await copyWithChecksum(src, dest);
        await fs.unlink(src);
      }
    } else {
      throw err;
    }
  }
}

module.exports = { sha256, copyWithChecksum, moveWithFallback };

if (require.main === module) {
  const os = require('os');
  const path = require('path');
  const tmp = os.tmpdir();
  const src = path.join(tmp, 'copy-move-test.txt');
  const dest = path.join(tmp, 'copy-move-out.txt');
  fs.writeFile(src, 'hello world').then(async () => {
    await copyWithChecksum(src, dest);
    console.log(`Copied ${src} -> ${dest}`);
    await moveWithFallback(dest, path.join(tmp, 'moved.txt'));
    console.log('Moved successfully');
  });
}
