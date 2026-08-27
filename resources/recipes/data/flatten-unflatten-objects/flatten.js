// Flatten and unflatten nested objects in JavaScript.
// Usage: node flatten.js

const fs = require("fs");

function flatten(obj, separator = ".", prefix = "") {
  const result = {};

  if (obj !== null && typeof obj === "object" && !Array.isArray(obj)) {
    for (const [key, value] of Object.entries(obj)) {
      const newKey = prefix ? `${prefix}${separator}${key}` : key;
      Object.assign(result, flatten(value, separator, newKey));
    }
  } else if (Array.isArray(obj)) {
    obj.forEach((value, index) => {
      const newKey = `${prefix}[${index}]`;
      Object.assign(result, flatten(value, separator, newKey));
    });
  } else {
    result[prefix] = obj;
  }

  return result;
}

function _set(node, parts, value) {
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    const nextIsIndex = /^\d+$/.test(parts[i + 1]);
    if (Array.isArray(node)) {
      const index = Number(part);
      while (node.length <= index) node.push(null);
      if (node[index] === null) {
        node[index] = nextIsIndex ? [] : {};
      }
      node = node[index];
    } else {
      if (!(part in node)) {
        node[part] = nextIsIndex ? [] : {};
      }
      node = node[part];
    }
  }

  const last = parts[parts.length - 1];
  if (Array.isArray(node)) {
    const index = Number(last);
    while (node.length <= index) node.push(null);
    node[index] = value;
  } else {
    node[last] = value;
  }
}

function unflatten(flat, separator = ".") {
  const result = {};
  const esc = separator.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const splitRe = new RegExp(`${esc}|[\\[\\]]`, "g");

  for (const [key, value] of Object.entries(flat)) {
    const parts = key.split(splitRe).filter(Boolean);
    _set(result, parts, value);
  }

  return result;
}

// Run
const nested = JSON.parse(fs.readFileSync("sample.json", "utf8"));

const flat = flatten(nested);
console.log("=== Flattened ===");
for (const [key, value] of Object.entries(flat)) {
  console.log(`  ${key}: ${value}`);
}

const restored = unflatten(flat);
console.log("\n=== Unflattened ===");
console.log(JSON.stringify(restored, null, 2));

// Verify round-trip
const flatAgain = flatten(restored);
const flatStr = JSON.stringify(flat);
const flatAgainStr = JSON.stringify(flatAgain);
if (flatStr !== flatAgainStr) {
  console.error("✗ Round-trip failed!");
  process.exit(1);
}
console.log("\n✓ Round-trip verified: flatten(unflatten(flat)) == flat");
