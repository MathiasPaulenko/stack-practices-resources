// Abstract Factory in Java: product interfaces, a Light family,
// and config-driven loading via reflection.
interface Button {
    String render();
}

interface Checkbox {
    String render();
}

class LightButton implements Button {
    public String render() { return "Light Button"; }
}

class LightCheckbox implements Checkbox {
    public String render() { return "Light Checkbox"; }
}

public interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class LightUIFactory implements UIFactory {
    public Button createButton() { return new LightButton(); }
    public Checkbox createCheckbox() { return new LightCheckbox(); }
}

class FactoryLoader {
    public static UIFactory loadFactory(String className)
            throws Exception {
        Class<?> clazz = Class.forName(className);
        return (UIFactory) clazz.getDeclaredConstructor().newInstance();
    }
}
