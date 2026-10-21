// Streaming CSV import with per-row validation and error collection.
// Usage: node import_csv.js sample-users.csv
// Requires: npm install csv-parser

const csv = require("csv-parser");
const fs = require("fs");

function importCsv(filePath) {
  return new Promise((resolve, reject) => {
    const valid = [], errors = [];
    let rowNum = 1;

    fs.createReadStream(filePath)
      .pipe(csv())
      .on("data", (row) => {
        rowNum++;
        const name = row.name && row.name.trim();
        const email = row.email && row.email.trim();
        if (!name || !email) {
          errors.push({ row: rowNum, error: "Missing required field" });
        } else {
          valid.push({ name, email, age: Number(row.age) || null });
        }
      })
      .on("end", () => resolve({ valid, errors }))
      .on("error", reject);
  });
}

const file = process.argv[2] || "sample-users.csv";
importCsv(file).then(({ valid, errors }) => {
  console.log(JSON.stringify({ valid: valid.length, errors }, null, 2));
});
