class Button extends UIComponent {
  constructor(theme: Theme, private label: string) { super(theme); }

  setTheme(theme: Theme): void {
    this.theme = theme;
  }

  render(): string { return this.theme.renderButton(this.label); }
}

let currentTheme: Theme = new LightTheme();
const button = new Button(currentTheme, "Submit");
console.log(button.render()); // Light theme

button.setTheme(new DarkTheme());
console.log(button.render()); // Dark theme
