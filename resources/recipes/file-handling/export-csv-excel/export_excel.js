// CSV and Excel export utilities — JavaScript examples

const { format } = require("fast-csv");
const XLSX = require("xlsx");
const express = require("express");

const rows = [
  { id: 1, name: "Alice", email: "alice@example.com" },
  { id: 2, name: "Bob", email: "bob@example.com" },
];

// Small dataset: in-memory CSV
function exportCsvInMemory(rows, outputPath) {
  const ws = fs.createWriteStream(outputPath);
  format.write(rows, { headers: true }).pipe(ws);
}

// Excel generation
function exportExcel(rows, outputPath) {
  const ws = XLSX.utils.json_to_sheet(rows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Users");
  XLSX.writeFile(wb, outputPath);
}

// CSV injection sanitization
function sanitizeCsvCell(value) {
  if (value && ["=", "+", "-", "@"].includes(value[0])) {
    return `'${value}`;
  }
  return value;
}

// Express.js streaming endpoint with error handling
function createExportServer(db) {
  const app = express();

  app.get("/export/users", async (req, res) => {
    res.setHeader("Content-Type", "text/csv");
    res.setHeader("Content-Disposition", "attachment; filename=users.csv");

    try {
      const cursor = db.collection("users").find({}, { batchSize: 1000 });
      const stream = cursor.stream();
      const csvStream = format({ headers: true });

      stream.on("error", (err) => {
        console.error("DB stream error:", err);
        if (!res.headersSent) res.status(500).send("Export failed");
        stream.destroy();
      });

      csvStream.on("error", (err) => {
        console.error("CSV stream error:", err);
        stream.destroy();
      });

      req.on("aborted", () => {
        stream.destroy();
        csvStream.destroy();
      });

      stream.pipe(csvStream).pipe(res);
    } catch (err) {
      if (!res.headersSent) res.status(500).json({ error: err.message });
    }
  });

  return app;
}

module.exports = { exportCsvInMemory, exportExcel, sanitizeCsvCell, createExportServer };

if (require.main === module) {
  const fs = require("fs");
  exportCsvInMemory(rows, "users.csv");
  console.log("Wrote users.csv");
  exportExcel(rows, "users.xlsx");
  console.log("Wrote users.xlsx");
}
