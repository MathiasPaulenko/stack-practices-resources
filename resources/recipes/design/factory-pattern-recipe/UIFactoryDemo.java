// Abstract Factory — consistent families of UI widgets per OS theme (Java).
// Compile & run: javac UIFactoryDemo.java && java UIFactoryDemo
interface Button { void render(); }
interface Checkbox { void check(); }

class WindowsButton implements Button {
    public void render() { System.out.println("Rendering Windows button"); }
}
class WindowsCheckbox implements Checkbox {
    public void check() { System.out.println("Checking Windows checkbox"); }
}
class MacButton implements Button {
    public void render() { System.out.println("Rendering Mac button"); }
}
class MacCheckbox implements Checkbox {
    public void check() { System.out.println("Checking Mac checkbox"); }
}

interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class WindowsUIFactory implements UIFactory {
    public Button createButton() { return new WindowsButton(); }
    public Checkbox createCheckbox() { return new WindowsCheckbox(); }
}
class MacUIFactory implements UIFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
}

class Application {
    private final Button button;
    private final Checkbox checkbox;
    Application(UIFactory factory) {
        this.button = factory.createButton();
        this.checkbox = factory.createCheckbox();
    }
    void renderUI() { button.render(); checkbox.check(); }
}

public class UIFactoryDemo {
    public static void main(String[] args) {
        UIFactory factory = System.getProperty("os.name").contains("Windows")
            ? new WindowsUIFactory()
            : new MacUIFactory();
        new Application(factory).renderUI();
    }
}
