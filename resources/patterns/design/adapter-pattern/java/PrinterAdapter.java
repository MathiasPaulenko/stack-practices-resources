class OldPrinter {
    void oldPrint(String text) {
        System.out.println("OldPrinter: " + text);
    }
}

interface ModernPrinter {
    void print(String text);
}

// Object adapter: implements the target interface, delegates to the adaptee.
class PrinterAdapter implements ModernPrinter {
    private final OldPrinter oldPrinter;

    PrinterAdapter(OldPrinter oldPrinter) {
        this.oldPrinter = oldPrinter;
    }

    public void print(String text) {
        oldPrinter.oldPrint(text);
    }

    public static void main(String[] args) {
        ModernPrinter printer = new PrinterAdapter(new OldPrinter());
        printer.print("Hello World"); // OldPrinter: Hello World
    }
}
