// Parameterized product creation: the factory carries shared config
// (theme, locale, accessibility) so every product in the family inherits it.
interface UIFactoryConfig {
  theme: 'light' | 'dark';
  locale: string;
  accessibility: boolean;
}

interface ConfigurableUIFactory {
  setConfig(config: Partial<UIFactoryConfig>): void;
  createButton(label: string): ConfiguredButton;
}

class ConfiguredButton {
  constructor(
    private label: string,
    private config: UIFactoryConfig
  ) {}

  render(): string {
    const themeClass = this.config.theme === 'dark' ? 'dark-mode' : 'light-mode';
    return `<button class="${themeClass}">${this.label}</button>`;
  }
}

export class ConfigurableWebFactory implements ConfigurableUIFactory {
  private config: UIFactoryConfig = {
    theme: 'light',
    locale: 'en',
    accessibility: false
  };

  setConfig(config: Partial<UIFactoryConfig>): void {
    this.config = { ...this.config, ...config };
  }

  createButton(label: string): ConfiguredButton {
    return new ConfiguredButton(label, this.config);
  }
}

if (require.main === module) {
  const factory = new ConfigurableWebFactory();
  factory.setConfig({ theme: 'dark' });
  console.log(factory.createButton('Save').render());
}
