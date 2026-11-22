import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class ThemeManager {
    private static final Map<String, ThemeManager> instances = new ConcurrentHashMap<>();
    private final String themeName;

    private ThemeManager(String themeName) {
        this.themeName = themeName;
        System.out.println("Created theme manager for " + themeName);
    }

    public static ThemeManager getInstance(String themeName) {
        // computeIfAbsent is atomic: no duplicate creation under concurrency
        return instances.computeIfAbsent(themeName, ThemeManager::new);
    }

    public String apply(String component) {
        return "[" + themeName + "] Styled " + component;
    }
}

// Usage
ThemeManager light = ThemeManager.getInstance("light");
ThemeManager dark = ThemeManager.getInstance("dark");
ThemeManager light2 = ThemeManager.getInstance("light");

System.out.println(light == light2); // true
System.out.println(light == dark);   // false
