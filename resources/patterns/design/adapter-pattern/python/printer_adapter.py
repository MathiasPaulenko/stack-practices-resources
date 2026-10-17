class OldPrinter:
    def old_print(self, text: str):
        print(f"OldPrinter: {text}")


class PrinterAdapter:
    """Object adapter: wraps OldPrinter behind the modern print() interface."""

    def __init__(self, old_printer: OldPrinter):
        self._old = old_printer

    def print(self, text: str):
        self._old.old_print(text)


class ModernPrinter:
    def print(self, text: str):
        print(f"ModernPrinter: {text}")


class BiDirectionalPrinterAdapter:
    """Two-way adapter: exposes both the target and the adaptee interface."""

    def __init__(self, old_printer: OldPrinter, new_printer: ModernPrinter):
        self._old = old_printer
        self._new = new_printer

    def print(self, text: str):
        self._old.old_print(text)

    def old_print(self, text: str):
        self._new.print(text)


if __name__ == "__main__":
    adapter = PrinterAdapter(OldPrinter())
    adapter.print("Hello World")  # OldPrinter: Hello World

    bi = BiDirectionalPrinterAdapter(OldPrinter(), ModernPrinter())
    bi.print("Hello")       # via ModernPrinter interface → OldPrinter
    bi.old_print("World")   # via OldPrinter interface → ModernPrinter
