// Parse YAML with js-yaml: npm install js-yaml
import yaml from "js-yaml";
import fs from "fs";

const doc = yaml.load(fs.readFileSync("config.yaml", "utf8"));

console.log("app:", doc.app.name, doc.app.version);
console.log("database host:", doc.database.host);
console.log("production:", doc.production);
console.log("staging:", doc.staging);
console.log("features:", doc.features);
