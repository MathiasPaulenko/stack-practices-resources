// Dynamic factory loading: resolve the concrete factory from config
// (plugin architectures, white-label builds, A/B of whole UI families).
import { UIFactory } from './ui_factory';

interface FactoryConfig {
  type: string;
  module: string;
  className: string;
}

export async function loadFactory(config: FactoryConfig): Promise<UIFactory> {
  const module = await import(config.module);
  const FactoryClass = module[config.className];
  return new FactoryClass();
}

const config: FactoryConfig = {
  type: 'ios',
  module: './ui_factory',
  className: 'MobileFactory'
};

loadFactory(config).then((factory) => {
  console.log(factory.createButton('Confirm').render());
});
