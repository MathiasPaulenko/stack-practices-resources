// Core Abstract Factory: product interfaces, Web and Mobile families,
// and a client (SettingsScreen) that works against the interface only.
interface Button {
  render(): string;
  onClick(handler: () => void): void;
}

interface Checkbox {
  render(): string;
  toggle(): void;
  isChecked(): boolean;
}

interface Dialog {
  show(): void;
  hide(): void;
  setTitle(title: string): void;
}

export interface UIFactory {
  createButton(label: string): Button;
  createCheckbox(label: string): Checkbox;
  createDialog(): Dialog;
}

// Web family
export class WebButton implements Button {
  constructor(private label: string) {}
  render(): string { return `<button>${this.label}</button>`; }
  onClick(handler: () => void): void { /* attach DOM listener */ }
}

export class WebCheckbox implements Checkbox {
  private checked = false;
  constructor(private label: string) {}
  render(): string { return `<label><input type="checkbox"> ${this.label}</label>`; }
  toggle(): void { this.checked = !this.checked; }
  isChecked(): boolean { return this.checked; }
}

export class WebDialog implements Dialog {
  private title = '';
  show(): void { console.log('Show web dialog:', this.title); }
  hide(): void { console.log('Hide web dialog'); }
  setTitle(title: string): void { this.title = title; }
}

export class WebFactory implements UIFactory {
  createButton(label: string): Button { return new WebButton(label); }
  createCheckbox(label: string): Checkbox { return new WebCheckbox(label); }
  createDialog(): Dialog { return new WebDialog(); }
}

// Mobile family
export class MobileButton implements Button {
  constructor(private label: string) {}
  render(): string { return `[Mobile Button: ${this.label}]`; }
  onClick(): void { /* native tap handler */ }
}

export class MobileCheckbox implements Checkbox {
  private checked = false;
  constructor(private label: string) {}
  render(): string { return `[Mobile Switch: ${this.label}]`; }
  toggle(): void { this.checked = !this.checked; }
  isChecked(): boolean { return this.checked; }
}

export class MobileDialog implements Dialog {
  private title = '';
  show(): void { console.log('Show mobile modal:', this.title); }
  hide(): void { console.log('Dismiss mobile modal'); }
  setTitle(title: string): void { this.title = title; }
}

export class MobileFactory implements UIFactory {
  createButton(label: string): Button { return new MobileButton(label); }
  createCheckbox(label: string): Checkbox { return new MobileCheckbox(label); }
  createDialog(): Dialog { return new MobileDialog(); }
}

// Client uses any factory uniformly
export class SettingsScreen {
  private button: Button;
  private checkbox: Checkbox;
  private dialog: Dialog;

  constructor(factory: UIFactory) {
    this.button = factory.createButton('Save');
    this.checkbox = factory.createCheckbox('Dark Mode');
    this.dialog = factory.createDialog();
    this.dialog.setTitle('Confirm');
  }

  render(): string {
    return `${this.button.render()} ${this.checkbox.render()}`;
  }
}

if (require.main === module) {
  const webScreen = new SettingsScreen(new WebFactory());
  const mobileScreen = new SettingsScreen(new MobileFactory());
  console.log(webScreen.render());
  console.log(mobileScreen.render());
}
