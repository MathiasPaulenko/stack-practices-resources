// Node.js: fast-xml-parser object mapping. Run: node parse-xml.mjs
// npm install fast-xml-parser
import { readFileSync } from "node:fs";
import { XMLParser } from "fast-xml-parser";

const xmlString = readFileSync(new URL("./data.xml", import.meta.url), "utf8");

const parser = new XMLParser({
  ignoreAttributes: false,
  attributeNamePrefix: "@_",
  processEntities: false, // keep XXE-safe defaults explicit
});

const doc = parser.parse(xmlString);
for (const item of doc.catalog.item) {
  console.log(item["@_id"], item["@_category"], item.name, item.price["#text"]);
}
