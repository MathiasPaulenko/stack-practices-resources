// Abstract Factory in JavaScript: product interfaces, a concrete
// family, and a lazy-initializing factory proxy.
class Button {
  render() {
    throw new Error("Not implemented");
  }
}

class Checkbox {
  render() {
    throw new Error("Not implemented");
  }
}

class LightButton extends Button {
  render() {
    return "Light Button";
  }
}

class LightCheckbox extends Checkbox {
  render() {
    return "Light Checkbox";
  }
}

class UIFactory {
  createButton() {
    throw new Error("Not implemented");
  }
  createCheckbox() {
    throw new Error("Not implemented");
  }
}

class LightUIFactory extends UIFactory {
  createButton() {
    return new LightButton();
  }
  createCheckbox() {
    return new LightCheckbox();
  }
}

// Lazy proxy: defers concrete factory instantiation until first use.
class LazyUIFactory extends UIFactory {
  constructor(factoryCreator) {
    super();
    this._factoryCreator = factoryCreator;
    this._factory = null;
  }

  _getFactory() {
    if (!this._factory) {
      this._factory = this._factoryCreator();
    }
    return this._factory;
  }

  createButton() {
    return this._getFactory().createButton();
  }

  createCheckbox() {
    return this._getFactory().createCheckbox();
  }
}

if (require.main === module) {
  const lazyFactory = new LazyUIFactory(() => {
    console.log('Factory initialized');
    return new LightUIFactory();
  });
  // Factory not initialized until first method call
  console.log(lazyFactory.createButton().render());
}
