// Offline, dependency-free version of the StackPractices recipe
// "CRUD Operations with MongoDB and Mongoose".
//
// Implements the same CRUD + soft-delete + transaction semantics the recipe
// teaches, against an in-memory document store, so it runs anywhere Node 18+
// is installed — no MongoDB or npm install needed.

export class DocumentStore {
  constructor() {
    this.docs = new Map();
    this.nextId = 1;
    this.validators = {};
  }

  addValidator(field, fn, message) {
    (this.validators[field] ??= []).push({ fn, message });
  }

  _validate(doc) {
    for (const [field, checks] of Object.entries(this.validators)) {
      for (const { fn, message } of checks) {
        if (!fn(doc[field])) throw new Error(`${field}: ${message}`);
      }
    }
  }

  create(data) {
    this._validate(data);
    const id = String(this.nextId++);
    const now = new Date();
    const doc = { _id: id, deletedAt: null, createdAt: now, updatedAt: now, ...data };
    this.docs.set(id, doc);
    return doc;
  }

  // Mimics the soft-delete plugin from the recipe: find() hides deleted docs
  // unless includeDeleted is set.
  find(filter = {}, { includeDeleted = false } = {}) {
    return [...this.docs.values()].filter((d) => {
      if (!includeDeleted && d.deletedAt !== null) return false;
      return Object.entries(filter).every(([k, v]) => d[k] === v);
    });
  }

  findById(id, opts = {}) {
    return this.find({ _id: id }, opts)[0] ?? null;
  }

  findByIdAndUpdate(id, patch) {
    const doc = this.docs.get(id);
    if (!doc || doc.deletedAt !== null) return null;
    this._validate({ ...doc, ...patch });
    Object.assign(doc, patch, { updatedAt: new Date() });
    return doc;
  }

  softDelete(id) {
    return this.findByIdAndUpdate(id, { deletedAt: new Date() });
  }

  countDocuments(filter = {}) {
    return this.find(filter).length;
  }

  // Mimics a multi-write transaction: all ops apply or none does.
  withTransaction(ops) {
    // Deep-copy docs so in-place mutation inside the tx can't leak back.
    const snapshot = new Map([...this.docs].map(([k, v]) => [k, { ...v }]));
    try {
      const results = ops.map((op) => op());
      return results;
    } catch (err) {
      this.docs = snapshot;
      throw err;
    }
  }
}

export function makeUserStore() {
  const store = new DocumentStore();
  store.addValidator('email', (v) => typeof v === 'string' && v.includes('@'), 'valid email is required');
  store.addValidator('name', (v) => typeof v === 'string' && v.length >= 2, 'min length 2');
  return store;
}
