// Template Method Pattern — data import pipeline.
// The base class owns the algorithm skeleton (importData); subclasses
// implement only the steps that vary. Run with: node template-method.js

class DataImporter {
  importData(source) {
    const raw = this.fetch(source);
    const parsed = this.parse(raw);
    const validated = this.validate(parsed);
    this.save(validated);
    this.onComplete();
  }

  fetch(source) {
    throw new Error("Subclasses must implement fetch()");
  }

  parse(raw) {
    throw new Error("Subclasses must implement parse()");
  }

  validate(data) {
    if (!data.id) throw new Error("Missing required field: id");
    return data;
  }

  save(data) {
    console.log("Saving:", data);
  }

  onComplete() {
    // Hook — subclasses may override
  }
}

class CSVImporter extends DataImporter {
  fetch(source) {
    return `CSV content from ${source}`;
  }

  parse(raw) {
    return { id: 1, format: "csv", content: raw };
  }
}

class JSONImporter extends DataImporter {
  fetch(source) {
    return `JSON content from ${source}`;
  }

  parse(raw) {
    return { id: 2, format: "json", content: raw };
  }

  onComplete() {
    console.log("JSON import completed!");
  }
}

new CSVImporter().importData("users.csv");
new JSONImporter().importData("users.json");
