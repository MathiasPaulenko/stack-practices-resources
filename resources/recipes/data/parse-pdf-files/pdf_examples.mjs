// Runnable examples for the "Parse PDF Files" recipe.
// Usage: npm install && node pdf_examples.mjs <example>
// Examples: text | metadata

import fs from "node:fs";

const SAMPLE = "sample.pdf"; // create it first with: python pdf_examples.py sample

async function text(path = SAMPLE) {
  // Import the lib entry point to avoid pdf-parse's debug-mode block.
  const pdfParse = (await import("pdf-parse/lib/pdf-parse.js")).default;
  const data = await pdfParse(fs.readFileSync(path));
  console.log(`Pages: ${data.numpages}`);
  console.log(data.text);
}

async function metadata(path = SAMPLE) {
  const { PDFDocument } = await import("pdf-lib");
  const pdfDoc = await PDFDocument.load(fs.readFileSync(path));
  console.log(`Pages: ${pdfDoc.getPageCount()}`);
  console.log("Title:", pdfDoc.getTitle());
  console.log("Author:", pdfDoc.getAuthor());
}

const EXAMPLES = { text, metadata };
const name = process.argv[2] ?? "text";
if (!EXAMPLES[name]) {
  console.log(`Unknown example. Choose from: ${Object.keys(EXAMPLES).join(", ")}`);
  process.exit(1);
}
await EXAMPLES[name]();
