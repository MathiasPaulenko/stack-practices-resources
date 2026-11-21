// Merge every .json file in a directory, in sorted order (last file wins).
const fs = require("fs");
const path = require("path");
const { deepMerge } = require("./mergeJson");

function mergeJsonDir(dir) {
  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .sort();
  let merged = {};
  const skipped = [];
  for (const file of files) {
    try {
      merged = deepMerge(
        merged,
        JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"))
      );
    } catch (err) {
      skipped.push({ file, error: err.message });
    }
  }
  return { merged, skipped };
}

module.exports = { mergeJsonDir };

if (require.main === module) {
  const dir = process.argv[2] || "./config";
  const { merged, skipped } = mergeJsonDir(dir);
  if (skipped.length) console.error("skipped:", skipped);
  console.log(JSON.stringify(merged, null, 2));
}
