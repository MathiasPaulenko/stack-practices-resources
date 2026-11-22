class Logger {
  static #instances = new Map();

  constructor(moduleName) {
    this.moduleName = moduleName;
    console.log(`Created logger for ${moduleName}`);
  }

  static getInstance(moduleName) {
    if (!Logger.#instances.has(moduleName)) {
      Logger.#instances.set(moduleName, new Logger(moduleName));
    }
    return Logger.#instances.get(moduleName);
  }

  log(message) {
    console.log(`[${this.moduleName}] ${message}`);
  }
}

// Usage
const dbLogger = Logger.getInstance('database');
const apiLogger = Logger.getInstance('api');
const dbLogger2 = Logger.getInstance('database');

console.log(dbLogger === dbLogger2); // true
console.log(dbLogger === apiLogger); // false
