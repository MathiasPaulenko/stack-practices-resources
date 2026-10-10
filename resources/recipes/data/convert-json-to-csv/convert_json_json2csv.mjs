#!/usr/bin/env node
// JSON-to-CSV with @json2csv (nested objects get flattened by the Parser).
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { Parser } from "@json2csv/plainjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const records = JSON.parse(
  fs.readFileSync(path.join(__dirname, "data", "sample_nested.json"), "utf-8")
);

// unwind explodes `orders` into one row per order
const parser = new Parser({ unwind: "orders" });
console.log(parser.parse(records));
