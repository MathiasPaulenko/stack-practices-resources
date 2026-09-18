/**
 * Twin Pattern — runnable TypeScript example.
 *
 * A `Widget` keeps the shared state and the public API. `Graphic` and
 * `Interactive` are the twins: each owns one concern and holds a
 * back-reference to the widget so it can read shared state.
 *
 * Run: npx tsx twin-widget.ts   (or compile with tsc and run node)
 */

/** Minimal surface a twin needs from its widget — injectable for tests. */
export interface WidgetLike {
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

function linked(w: WidgetLike | null, twin: string): WidgetLike {
  if (!w) throw new Error(`${twin} twin is not linked to a widget`);
  return w;
}

/** Twin A: drawing behavior. */
export class Graphic {
  widget: WidgetLike | null = null;

  draw(): string {
    const w = linked(this.widget, 'Graphic');
    return `Drawing ${w.name} at (${w.x}, ${w.y})`;
  }

  resize(width: number, height: number): string {
    const w = linked(this.widget, 'Graphic');
    w.width = width;
    w.height = height;
    return `Resized to ${width}x${height}`;
  }
}

/** Twin B: interaction behavior. */
export class Interactive {
  widget: WidgetLike | null = null;

  onClick(): string {
    return `Clicked on ${linked(this.widget, 'Interactive').name}`;
  }

  onHover(): string {
    return `Hovering over ${linked(this.widget, 'Interactive').name}`;
  }
}

/** The composite twin class that links Graphic and Interactive. */
export class Widget implements WidgetLike {
  width = 100;
  height = 50;

  private graphic = new Graphic();
  private interactive = new Interactive();

  constructor(
    public name: string,
    public x = 0,
    public y = 0,
  ) {
    this.graphic.widget = this;
    this.interactive.widget = this;
  }

  draw(): string {
    return this.graphic.draw();
  }

  resize(width: number, height: number): string {
    return this.graphic.resize(width, height);
  }

  onClick(): string {
    return this.interactive.onClick();
  }

  onHover(): string {
    return this.interactive.onHover();
  }

  getGraphic(): Graphic {
    return this.graphic;
  }

  getInteractive(): Interactive {
    return this.interactive;
  }
}

const isMain = process.argv[1]?.endsWith('twin-widget.ts')
  || process.argv[1]?.endsWith('twin-widget.js');

if (isMain) {
  const button = new Widget('SubmitButton', 10, 20);
  console.log(button.draw());
  console.log(button.onClick());
  console.log(button.onHover());
  console.log(button.resize(200, 60));
}
