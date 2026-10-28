// bridge/Renderer.ts
interface UIRenderer {
  renderButton(label: string, onClick: () => void): string;
  renderCheckbox(label: string, checked: boolean): string;
  renderSlider(min: number, max: number, value: number): string;
}

// Implementations
class WebRenderer implements UIRenderer {
  renderButton(label: string, onClick: () => void): string {
    return `<button onclick="${onClick.name}()">${label}</button>`;
  }

  renderCheckbox(label: string, checked: boolean): string {
    const checkedAttr = checked ? 'checked' : '';
    return `<label><input type="checkbox" ${checkedAttr}> ${label}</label>`;
  }

  renderSlider(min: number, max: number, value: number): string {
    return `<input type="range" min="${min}" max="${max}" value="${value}">`;
  }
}

class NativeRenderer implements UIRenderer {
  renderButton(label: string): string {
    return `[Native Button: ${label}]`;
  }

  renderCheckbox(label: string, checked: boolean): string {
    return `[Native Checkbox: ${label} ${checked ? '✓' : ' '}]`;
  }

  renderSlider(min: number, max: number, value: number): string {
    return `[Native Slider: ${value}/${max}]`;
  }
}

// Abstractions
abstract class UIComponent {
  constructor(protected renderer: UIRenderer) {}
  abstract render(): string;
}

class Button extends UIComponent {
  constructor(
    renderer: UIRenderer,
    private label: string,
    private onClick: () => void
  ) {
    super(renderer);
  }

  render(): string {
    return this.renderer.renderButton(this.label, this.onClick);
  }
}

class Checkbox extends UIComponent {
  constructor(
    renderer: UIRenderer,
    private label: string,
    private checked: boolean
  ) {
    super(renderer);
  }

  render(): string {
    return this.renderer.renderCheckbox(this.label, this.checked);
  }
}

// Usage
function submitForm(): void { /* ... */ }

const webButton = new Button(new WebRenderer(), 'Submit', submitForm);
const nativeButton = new Button(new NativeRenderer(), 'Submit', submitForm);

console.log(webButton.render());     // <button onclick="submitForm()">Submit</button>
console.log(nativeButton.render());  // [Native Button: Submit]
