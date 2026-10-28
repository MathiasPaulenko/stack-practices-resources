class DarkTheme implements Theme {
  primary = "#1e293b";
  background = "#0f172a";
  text = "#f8fafc";
  renderButton(label: string): string {
    return `<button style="background:${this.primary};color:${this.text};padding:10px 20px;border:1px solid ${this.text}">${label}</button>`;
  }
}
