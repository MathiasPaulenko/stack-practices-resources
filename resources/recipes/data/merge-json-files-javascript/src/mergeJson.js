// Dependency-free deep merge hardened against null and prototype pollution.
const isPlainObject = (v) =>
  v !== null && typeof v === "object" && !Array.isArray(v);
const UNSAFE_KEYS = new Set(["__proto__", "constructor", "prototype"]);

function deepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (UNSAFE_KEYS.has(key)) continue;
    if (isPlainObject(source[key]) && isPlainObject(target[key])) {
      deepMerge(target[key], source[key]);
    } else {
      target[key] = isPlainObject(source[key])
        ? deepMerge({}, source[key])
        : source[key];
    }
  }
  return target;
}

module.exports = { deepMerge, isPlainObject };

if (require.main === module) {
  const defaults = { api: { timeout: 5000, retries: 3 }, log: { level: "info" } };
  const user = { api: { timeout: 10000 }, log: { format: "json" }, extra: null };
  console.log(JSON.stringify(deepMerge({}, deepMerge(defaults, user)), null, 2));
}
