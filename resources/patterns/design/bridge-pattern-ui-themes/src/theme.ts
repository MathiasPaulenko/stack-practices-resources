// bridge/Theme.ts
interface Theme {
  getColors(): { primary: string; background: string; text: string };
  getBorderRadius(): number;
  getSpacing(): number;
}

class LightTheme implements Theme {
  getColors() { return { primary: '#007bff', background: '#ffffff', text: '#333333' }; }
  getBorderRadius() { return 4; }
  getSpacing() { return 8; }
}

class DarkTheme implements Theme {
  getColors() { return { primary: '#4dabf7', background: '#1a1a1a', text: '#e0e0e0' }; }
  getBorderRadius() { return 8; }
  getSpacing() { return 12; }
}

abstract class ThemedComponent {
  constructor(protected theme: Theme) {}
}

class ThemedButton extends ThemedComponent {
  render(label: string): string {
    const colors = this.theme.getColors();
    return `
      <button style="
        background: ${colors.primary};
        color: ${colors.text};
        border-radius: ${this.theme.getBorderRadius()}px;
        padding: ${this.theme.getSpacing()}px;
      ">${label}</button>
    `;
  }
}

const light = new ThemedButton(new LightTheme());
const dark = new ThemedButton(new DarkTheme());
