class OldPrinter {
  oldPrint(text) {
    console.log(`OldPrinter: ${text}`);
  }
}

// Object adapter: wraps OldPrinter behind the modern print() interface.
class PrinterAdapter {
  constructor(oldPrinter) {
    this.old = oldPrinter;
  }

  print(text) {
    this.old.oldPrint(text);
  }
}

// Usage
const adapter = new PrinterAdapter(new OldPrinter());
adapter.print("Hello World"); // OldPrinter: Hello World
