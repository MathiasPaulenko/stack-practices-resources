// Runnable Excel (.xlsx) examples with SheetJS (xlsx).
//
// Companion to https://stackpractices.com/recipes/parse-excel-files/
//
// Usage:
//   npm install
//   node excel_parse.mjs sample   # creates sample.xlsx (run this first)
//   node excel_parse.mjs read     # read rows from sample.xlsx
//   node excel_parse.mjs write    # write output.xlsx

import xlsx from "xlsx";

const [, , cmd] = process.argv;

function sample() {
  const ws = xlsx.utils.aoa_to_sheet([
    ["Product", "Quantity", "Price"],
    ["Widget", 100, 19.99],
    ["Gadget", 40, 4.5],
    ["Sprocket", 12, 9.75],
  ]);
  const wb = xlsx.utils.book_new();
  xlsx.utils.book_append_sheet(wb, ws, "Sales");
  xlsx.writeFile(wb, "sample.xlsx");
  console.log("Created sample.xlsx");
}

function read() {
  const wb = xlsx.readFile("sample.xlsx");
  const sheet = wb.Sheets[wb.SheetNames[0]];
  console.log(xlsx.utils.sheet_to_json(sheet));
}

function write() {
  const ws = xlsx.utils.aoa_to_sheet([
    ["Name", "Age"],
    ["Alice", 30],
  ]);
  const wb = xlsx.utils.book_new();
  xlsx.utils.book_append_sheet(wb, ws, "People");
  xlsx.writeFile(wb, "output.xlsx");
  console.log("Created output.xlsx");
}

const commands = { sample, read, write };

if (commands[cmd]) {
  commands[cmd]();
} else {
  console.log("Usage: node excel_parse.mjs [sample|read|write]");
}
