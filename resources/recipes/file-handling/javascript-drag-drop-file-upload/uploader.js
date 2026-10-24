/**
 * DragDropUploader — production class from the recipe.
 * Usage: new DragDropUploader("drop-zone", { uploadUrl: "/api/upload", ... })
 *
 * SimulatedUploader — same API, but fakes the upload with a timer so the
 * demo in index.html runs with no backend. Drop it in only for testing.
 */
class DragDropUploader {
    constructor(elementId, options = {}) {
        this.dropZone = document.getElementById(elementId);
        this.maxSize = options.maxSize ?? 5 * 1024 * 1024;
        this.allowedTypes = options.allowedTypes ?? ["image/jpeg", "image/png", "image/webp"];
        this.uploadUrl = options.uploadUrl ?? "/api/upload";
        this.onProgress = options.onProgress ?? (() => {});
        this.onComplete = options.onComplete ?? (() => {});
        this.onError = options.onError ?? (() => {});

        this.setupEvents();
    }

    setupEvents() {
        this.dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            this.dropZone.classList.add("drag-over");
        });

        this.dropZone.addEventListener("dragleave", (e) => {
            if (!this.dropZone.contains(e.relatedTarget)) {
                this.dropZone.classList.remove("drag-over");
            }
        });

        this.dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            this.dropZone.classList.remove("drag-over");
            this.handleEntries(e.dataTransfer);
        });

        this.dropZone.addEventListener("click", () => {
            const input = document.createElement("input");
            input.type = "file";
            input.multiple = true;
            input.accept = this.allowedTypes.join(",");
            input.addEventListener("change", () => {
                this.handleFiles(Array.from(input.files));
            });
            input.click();
        });
    }

    handleEntries(dataTransfer) {
        let handled = false;
        for (const item of dataTransfer.items) {
            const entry = item.webkitGetAsEntry && item.webkitGetAsEntry();
            if (entry && entry.isDirectory) {
                handled = true;
                this.walkEntry(entry);
            }
        }
        if (!handled) {
            this.handleFiles(Array.from(dataTransfer.files));
        }
    }

    walkEntry(entry) {
        if (entry.isFile) {
            entry.file(file => this.handleFiles([file]));
            return;
        }
        const reader = entry.createReader();
        const readBatch = () => {
            // readEntries returns max 100 entries per call
            reader.readEntries(entries => {
                if (entries.length === 0) return;
                entries.forEach(child => this.walkEntry(child));
                readBatch();
            });
        };
        readBatch();
    }

    handleFiles(files) {
        for (const file of files) {
            const error = this.validate(file);
            if (error) {
                this.onError(file, error);
                continue;
            }
            if (file.type.startsWith("image/")) this.preview(file);
            this.upload(file);
        }
    }

    validate(file) {
        if (!this.allowedTypes.includes(file.type)) {
            return `Invalid type: ${file.type}`;
        }
        if (file.size > this.maxSize) {
            return `File too large: ${this.formatSize(file.size)}`;
        }
        return null;
    }

    upload(file) {
        const formData = new FormData();
        formData.append("file", file);

        const xhr = new XMLHttpRequest();
        this._xhr = xhr;

        xhr.upload.addEventListener("progress", (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                this.onProgress(file, percent);
            }
        });

        xhr.addEventListener("load", () => {
            if (xhr.status === 200) {
                this.onComplete(file, JSON.parse(xhr.responseText));
            } else {
                this.onError(file, `Upload failed: ${xhr.status}`);
            }
        });

        xhr.addEventListener("error", () => {
            this.onError(file, "Network error");
        });

        xhr.open("POST", this.uploadUrl);
        xhr.send(formData);
    }

    preview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const grid = document.getElementById("preview-grid");
            if (!grid) return;
            const img = document.createElement("img");
            img.src = e.target.result;
            img.alt = file.name;
            grid.appendChild(img);
        };
        reader.readAsDataURL(file);
    }

    formatSize(bytes) {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }
}

/** Simulated upload: same callbacks, fake progress. For the local demo only. */
class SimulatedUploader extends DragDropUploader {
    upload(file) {
        let percent = 0;
        const timer = setInterval(() => {
            percent = Math.min(100, percent + 5 + Math.random() * 10);
            this.onProgress(file, Math.round(percent));
            if (percent >= 100) {
                clearInterval(timer);
                this.onComplete(file, { ok: true, simulated: true });
            }
        }, 80);
    }
}
