// Lazy factory proxy: defer concrete factory instantiation until
// first product creation (heavy init, rare code paths).
import { UIFactory, WebFactory } from './ui_factory';

export class LazyUIFactory implements UIFactory {
  private factory: UIFactory | null = null;

  constructor(private factoryFactory: () => UIFactory) {}

  private getFactory(): UIFactory {
    if (!this.factory) {
      this.factory = this.factoryFactory();
    }
    return this.factory;
  }

  createButton(label: string) { return this.getFactory().createButton(label); }
  createCheckbox(label: string) { return this.getFactory().createCheckbox(label); }
  createDialog() { return this.getFactory().createDialog(); }
}

if (require.main === module) {
  const lazyFactory = new LazyUIFactory(() => {
    console.log('Initializing WebFactory...');
    return new WebFactory();
  });
  // Factory not initialized until first method call
  console.log(lazyFactory.createButton('Click me').render());
}
