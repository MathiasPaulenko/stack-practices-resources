/**
 * Flyweight pattern applied to text rendering (the canonical GoF example).
 *
 * A document with thousands of characters shares a handful of CharacterStyle
 * flyweights instead of duplicating style data on every glyph. Position stays
 * extrinsic: it is passed to render() at call time.
 */

interface CharacterStyle {
  font: string;
  size: number;
  color: string;
  bold: boolean;
}

class StyleFactory {
  private styles = new Map<string, CharacterStyle>();

  getStyle(font: string, size: number, color: string, bold: boolean): CharacterStyle {
    const key = `${font}-${size}-${color}-${bold}`;
    if (!this.styles.has(key)) {
      this.styles.set(key, { font, size, color, bold });
    }
    return this.styles.get(key)!;
  }

  getStyleCount(): number {
    return this.styles.size;
  }
}

class Character {
  constructor(
    private char: string,
    private style: CharacterStyle // shared intrinsic state
  ) {}

  render(position: number): string {
    // extrinsic state passed at render time
    const css = `font:${this.style.size}px ${this.style.font};color:${this.style.color}`;
    return `<span style="${css}" data-pos="${position}">${this.char}</span>`;
  }
}

class Document {
  private characters: { char: Character; position: number }[] = [];
  private styleFactory = new StyleFactory();

  insert(char: string, position: number, font: string, size: number, color: string, bold: boolean): void {
    const style = this.styleFactory.getStyle(font, size, color, bold);
    this.characters.push({ char: new Character(char, style), position });
  }

  render(): string {
    return this.characters.map((c) => c.char.render(c.position)).join("");
  }

  getMemoryStats(): { characters: number; uniqueStyles: number } {
    return {
      characters: this.characters.length,
      uniqueStyles: this.styleFactory.getStyleCount(),
    };
  }
}

// Usage: 10,000 characters rendered with only 2 unique styles
const doc = new Document();
doc.insert("H", 0, "Arial", 12, "#000", true);
doc.insert("e", 1, "Arial", 12, "#000", true);
for (let i = 2; i < 10000; i++) {
  doc.insert("x", i, "Arial", 12, "#000", false);
}

console.log(doc.getMemoryStats());
// { characters: 10000, uniqueStyles: 2 }
console.log(doc.render().slice(0, 200));

export { Character, CharacterStyle, Document, StyleFactory };
