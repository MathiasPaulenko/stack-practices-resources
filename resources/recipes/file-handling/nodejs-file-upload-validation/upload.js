// Complete upload-validation pipeline for Express + multer 2.x.
// Layers: size/count limits -> extension + MIME filter -> file-type signature check.
// Run:  npm install express multer@^2 file-type && node upload.js

const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");

const app = express();

const CONFIG = {
    maxFileSize: 5 * 1024 * 1024,
    maxFiles: 5,
    allowedMimetypes: ["image/jpeg", "image/png", "image/webp", "application/pdf"],
    allowedExtensions: [".jpg", ".jpeg", ".png", ".webp", ".pdf"],
    uploadDir: "uploads/"
};

// Overrides merge into CONFIG, so callers only declare what changes
function createUploadMiddleware(overrides = {}) {
    const config = { ...CONFIG, ...overrides };

    const fileFilter = (req, file, cb) => {
        const ext = path.extname(file.originalname).toLowerCase();
        if (!config.allowedMimetypes.includes(file.mimetype)) {
            return cb(new Error(`MIME type ${file.mimetype} not allowed`), false);
        }
        if (!config.allowedExtensions.includes(ext)) {
            return cb(new Error(`Extension ${ext} not allowed`), false);
        }
        cb(null, true);
    };

    const storage = multer.diskStorage({
        destination: (req, file, cb) => {
            fs.mkdirSync(config.uploadDir, { recursive: true });
            cb(null, config.uploadDir);
        },
        filename: (req, file, cb) => {
            const safeName = path.basename(file.originalname)
                .replace(/[^a-zA-Z0-9.-]/g, "_")
                .substring(0, 100);
            cb(null, `${Date.now()}-${safeName}`);
        }
    });

    return multer({
        storage,
        limits: { fileSize: config.maxFileSize, files: config.maxFiles },
        fileFilter
    });
}

const uploadMiddleware = createUploadMiddleware();

app.post("/api/documents", uploadMiddleware.array("files", 5), async (req, res) => {
    const { fileTypeFromFile } = await import("file-type");

    for (const f of req.files) {
        const detected = await fileTypeFromFile(f.path);
        if (!detected || !CONFIG.allowedMimetypes.includes(detected.mime)) {
            fs.unlinkSync(f.path);
            return res.status(415).json({
                error: `${f.originalname}: content not allowed`,
                detected: detected ? detected.mime : null
            });
        }
    }

    res.json({
        uploaded: req.files.map(f => ({ filename: f.filename, size: f.size }))
    });
});

// Multer errors and fileFilter errors land in the same middleware — tell them apart
app.use((err, req, res, next) => {
    if (err instanceof multer.MulterError) {
        const status = err.code === "LIMIT_FILE_SIZE" ? 413 : 400;
        return res.status(status).json({ error: err.message, code: err.code });
    }
    if (err) {
        return res.status(400).json({ error: err.message });
    }
    next();
});

app.listen(3000, () => console.log("Listening on http://localhost:3000"));
