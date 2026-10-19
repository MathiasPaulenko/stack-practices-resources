// Read secrets with the _FILE convention, with env var fallback for local dev.
const fs = require("fs");

function getSecret(name) {
  const filePath = process.env[`${name}_FILE`];
  if (filePath) {
    return fs.readFileSync(filePath, "utf8").trim();
  }
  return process.env[name] || "";
}

console.log("DB password loaded:", Boolean(getSecret("DB_PASSWORD")));
