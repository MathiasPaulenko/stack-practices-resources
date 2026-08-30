#!/usr/bin/env node
// Convert CSV to JSON using csv-parse with async iteration (Node 18+).
import fs from "fs";
import path from "path";
import { parse } from "csv-parse";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const csvPath = path.join(__dirname, "data", "sample.csv");

const csv = fs.createReadStream(csvPath);
const parser = csv.pipe(
  parse({
    columns: true,
    cast: (value, context) => {
      if (context.column === "age") return Number(value);
      if (context.column === "active") return value.toLowerCase() === "true";
      return value;
    },
  })
);

const rows = [];
for await (const row of parser) {
  rows.push(row);
}
console.log(JSON.stringify(rows, null, 2));
