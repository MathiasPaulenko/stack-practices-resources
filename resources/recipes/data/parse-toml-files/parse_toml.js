// Parse and write TOML files in JavaScript.
// Requires: npm install @iarna/toml
import toml from "@iarna/toml";
import fs from "fs";

function readToml(path) {
  const content = fs.readFileSync(path, "utf8");
  return toml.parse(content);
}

function writeToml(data, path) {
  const content = toml.stringify(data);
  fs.writeFileSync(path, content, "utf8");
}

function deepMerge(base, override) {
  const result = { ...base };
  for (const [key, value] of Object.entries(override)) {
    if (
      key in result &&
      typeof result[key] === "object" &&
      !Array.isArray(result[key]) &&
      typeof value === "object" &&
      !Array.isArray(value)
    ) {
      result[key] = deepMerge(result[key], value);
    } else {
      result[key] = value;
    }
  }
  return result;
}

// Example usage
const config = readToml("config.toml");
console.log(config.app.name);
console.log(config.database.host);
console.log(config.servers?.length ?? 0);
