#!/usr/bin/env node
// Convert CSV to JSON in Node using PapaParse.
import fs from "fs";
import path from "path";
import Papa from "papaparse";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const csvPath = path.join(__dirname, "data", "sample.csv");

const file = fs.readFileSync(csvPath, "utf-8");
const result = Papa.parse(file, {
  header: true,
  transform: (value, field) => {
    if (field === "age") return Number(value);
    if (field === "active") return value.toLowerCase() === "true";
    return value;
  },
});

console.log(JSON.stringify(result.data, null, 2));
