#!/usr/bin/env node
// Manual JSON-to-CSV conversion for flat arrays (no dependencies).
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const records = JSON.parse(
  fs.readFileSync(path.join(__dirname, "data", "sample.json"), "utf-8")
);

const headers = Object.keys(records[0]);
const rows = records.map((r) =>
  headers.map((h) => JSON.stringify(r[h] ?? "")).join(",")
);
const csv = [headers.join(","), ...rows].join("\n");

console.log(csv);
