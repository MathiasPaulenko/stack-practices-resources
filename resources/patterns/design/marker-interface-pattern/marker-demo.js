// Marker Interface Pattern — JavaScript demo
// JavaScript has no interfaces; Symbol keys act as unique markers.
// Run: node marker-demo.js

const Serializable = Symbol('Serializable');
const Cloneable = Symbol('Cloneable');

class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }

  // Mark this class as Serializable and Cloneable
  static [Serializable] = true;
  static [Cloneable] = true;
}

class SecretData {
  constructor(data) {
    this.data = data;
  }
  // Not marked as Serializable
}

class Serializer {
  static safeSerialize(obj) {
    const constructor = obj.constructor;
    if (constructor[Serializable]) {
      return JSON.stringify(obj);
    }
    throw new TypeError(`Object of type ${constructor.name} is not Serializable`);
  }

  static safeClone(obj) {
    const constructor = obj.constructor;
    if (constructor[Cloneable]) {
      return JSON.parse(JSON.stringify(obj));
    }
    throw new TypeError(`Object of type ${constructor.name} is not Cloneable`);
  }
}

const user = new User('Alice', 'alice@example.com');
const json = Serializer.safeSerialize(user);
console.log('Serialized:', json);

try {
  Serializer.safeSerialize(new SecretData('top-secret'));
} catch (e) {
  console.error('Rejected:', e.message);
}
