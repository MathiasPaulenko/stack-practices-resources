/**
 * Prototype pattern — a named registry of clonable objects.
 *
 * `PrototypeRegistry` maps keys to configured prototype instances and
 * hands out a fresh clone on every `get()`. Callers never see a concrete
 * class or constructor — just a key and an independent copy.
 *
 * Run the demo:   node prototype.js
 * Run the tests:  node --test prototype.test.js
 */

class ProductConfig {
  constructor(name, price, category, attributes = {}, tags = []) {
    this.name = name;
    this.price = price;
    this.category = category;
    this.attributes = attributes;
    this.tags = tags;
  }

  // NOTE: structuredClone() would return a plain object and drop the
  // prototype chain (instanceof fails, methods disappear). A manual
  // clone keeps the class.
  clone() {
    return new ProductConfig(
      this.name,
      this.price,
      this.category,
      { ...this.attributes },
      [...this.tags]
    );
  }

  setAttribute(key, value) {
    this.attributes[key] = value;
    return this;
  }

  addTag(tag) {
    this.tags.push(tag);
    return this;
  }
}

class PrototypeRegistry {
  #prototypes = new Map();

  register(key, prototype) {
    if (typeof prototype.clone !== 'function') {
      throw new TypeError(`Prototype '${key}' must implement clone()`);
    }
    this.#prototypes.set(key, prototype);
  }

  get(key) {
    const proto = this.#prototypes.get(key);
    return proto ? proto.clone() : undefined;
  }

  keys() {
    return [...this.#prototypes.keys()];
  }
}

if (require.main === module) {
  const registry = new PrototypeRegistry();
  registry.register(
    'pro',
    new ProductConfig('Pro', 29.99, 'software', { tier: 'pro', support: '24h' }, ['pro', 'priority'])
  );

  const custom = registry.get('pro');
  custom.name = 'Pro Custom';
  custom.setAttribute('discount', '20%').addTag('custom');

  const original = registry.get('pro');
  console.log(`custom:   ${custom.name} attrs=${JSON.stringify(custom.attributes)} tags=${custom.tags}`);
  console.log(`original: ${original.name} attrs=${JSON.stringify(original.attributes)} tags=${original.tags}`);
  console.log(`independent: ${custom.attributes !== original.attributes}`);
}

module.exports = { ProductConfig, PrototypeRegistry };
