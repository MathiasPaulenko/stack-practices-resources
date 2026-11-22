// Avatar upload: memoryStorage + Sharp dimension check + EXIF strip via re-encode.
// Run:  npm install express multer@^2 sharp && node avatar.js

const express = require("express");
const multer = require("multer");
const sharp = require("sharp");

const app = express();

const upload = multer({
    storage: multer.memoryStorage(),
    limits: { fileSize: 5 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
        if (file.mimetype.startsWith("image/")) {
            cb(null, true);
        } else {
            cb(new Error("Only images allowed"), false);
        }
    }
});

app.post("/api/avatar", upload.single("avatar"), async (req, res) => {
    try {
        const metadata = await sharp(req.file.buffer).metadata();

        if (metadata.width > 2000 || metadata.height > 2000) {
            return res.status(400).json({
                error: "Image too large. Max dimensions: 2000x2000",
                actual: `${metadata.width}x${metadata.height}`
            });
        }
        if (metadata.width < 100 || metadata.height < 100) {
            return res.status(400).json({
                error: "Image too small. Min dimensions: 100x100",
                actual: `${metadata.width}x${metadata.height}`
            });
        }

        // Re-encoding also strips EXIF metadata (incl. GPS) users rarely mean to share
        const processedImage = await sharp(req.file.buffer)
            .resize(256, 256, { fit: "cover" })
            .jpeg({ quality: 80 })
            .toBuffer();

        res.json({
            message: "Avatar uploaded",
            original: `${metadata.width}x${metadata.height}`,
            processed: "256x256",
            bytes: processedImage.length
        });
    } catch (err) {
        res.status(400).json({ error: "Invalid image file" });
    }
});

app.listen(3000, () => console.log("Listening on http://localhost:3000"));
