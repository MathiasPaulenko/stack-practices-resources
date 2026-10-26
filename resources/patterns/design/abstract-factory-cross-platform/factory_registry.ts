// Factory registry: pick the concrete factory at runtime from a key,
// keeping detection in one place (bootstrap) instead of per-view checks.
import { UIFactory, WebFactory, MobileFactory } from './ui_factory';

interface FactoryRegistry {
  register(key: string, factory: UIFactory): void;
  get(key: string): UIFactory;
}

export class UIFactoryRegistry implements FactoryRegistry {
  private factories = new Map<string, UIFactory>();

  register(key: string, factory: UIFactory): void {
    this.factories.set(key, factory);
  }

  get(key: string): UIFactory {
    const factory = this.factories.get(key);
    if (!factory) throw new Error(`Factory not found: ${key}`);
    return factory;
  }
}

export function detectPlatform(): string {
  // In production this reads the environment (UA, native bridge, build flag).
  return 'web';
}

if (require.main === module) {
  const registry = new UIFactoryRegistry();
  registry.register('web', new WebFactory());
  registry.register('mobile', new MobileFactory());

  const platform = detectPlatform();
  const factory = registry.get(platform);
  console.log(factory.createButton('Save').render());
}
