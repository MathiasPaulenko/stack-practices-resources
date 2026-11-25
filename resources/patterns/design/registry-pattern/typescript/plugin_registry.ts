/**
 * Plugin registry: store and retrieve implementations by key, with lazy factories.
 * Advanced scenario from the Registry Pattern page.
 *
 * Run: npx tsx plugin_registry.ts   (or compile with tsc)
 */

interface Plugin {
  name: string;
  init(config: unknown): Promise<void>;
  execute(input: unknown): Promise<unknown>;
}

class PluginRegistry {
  private plugins = new Map<string, Plugin>();
  private factories = new Map<string, () => Plugin>();

  register(plugin: Plugin): void {
    if (this.plugins.has(plugin.name)) {
      throw new Error(`Plugin ${plugin.name} already registered`);
    }
    this.plugins.set(plugin.name, plugin);
  }

  registerFactory(name: string, factory: () => Plugin): void {
    this.factories.set(name, factory);
  }

  get(name: string): Plugin | undefined {
    if (this.plugins.has(name)) return this.plugins.get(name);
    const factory = this.factories.get(name);
    if (factory) {
      const plugin = factory();
      this.plugins.set(name, plugin);
      return plugin;
    }
    return undefined;
  }

  list(): string[] {
    return [...new Set([...this.plugins.keys(), ...this.factories.keys()])];
  }

  unregister(name: string): void {
    this.plugins.delete(name);
    this.factories.delete(name);
  }
}

function toCSV(rows: unknown): string {
  if (!Array.isArray(rows)) return "";
  return rows.map((row) => Object.values(row as object).join(",")).join("\n");
}

class PDFExportPlugin implements Plugin {
  name = "pdf";
  async init(): Promise<void> {}
  async execute(input: unknown): Promise<string> {
    return `PDF(${JSON.stringify(input).length} bytes)`;
  }
}

async function main(): Promise<void> {
  const data = [{ id: 1, user: "ada" }, { id: 2, user: "grace" }];

  const registry = new PluginRegistry();
  registry.register({
    name: "csv",
    init: async () => {},
    execute: async (input) => toCSV(input),
  });
  registry.register({
    name: "json",
    init: async () => {},
    execute: async (input) => JSON.stringify(input),
  });
  registry.registerFactory("pdf", () => new PDFExportPlugin());

  const exporter = registry.get("csv");
  if (exporter) {
    await exporter.init({ delimiter: "," });
    console.log(await exporter.execute(data));
  }

  const pdf = registry.get("pdf");
  console.log(await pdf?.execute(data));

  console.log("registered:", registry.list());
}

main();
