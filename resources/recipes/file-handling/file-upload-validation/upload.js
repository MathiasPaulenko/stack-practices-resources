// Multer setup + magic-bytes verification for Express.
// file-type is ESM-only since v19 — on CommonJS either pin file-type@18
// or load it dynamically inside an async context (as done here).
// See https://stackpractices.com/recipes/file-upload-validation/
const path = require('path');
const multer = require('multer');

const ALLOWED = { png: 'image/png', jpg: 'image/jpeg', pdf: 'application/pdf' };
const MAX_SIZE = 5 * 1024 * 1024;

const upload = multer({
  limits: { fileSize: MAX_SIZE },
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase().replace('.', '');
    if (!ALLOWED[ext]) return cb(new Error('Extension not allowed'));
    cb(null, true);
  },
});

async function validateBuffer(buffer, ext) {
  const { fileTypeFromBuffer } = await import('file-type');
  const type = await fileTypeFromBuffer(buffer);
  if (!type || type.mime !== ALLOWED[ext]) {
    throw new Error(`MIME mismatch: ${type?.mime}`);
  }
  return true;
}

// async function stripExif(inputBuffer) {
//   const sharp = require('sharp');
//   // sharp drops EXIF/ICC unless you call .withMetadata()
//   return sharp(inputBuffer).rotate().png().toBuffer();
// }

module.exports = { upload, validateBuffer };
