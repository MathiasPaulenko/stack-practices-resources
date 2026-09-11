// FlyweightJava.java — Flyweight pattern implementation in Java.
// Compile: javac FlyweightJava.java
// Run: java FlyweightJava

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.ArrayList;
import java.util.List;

final class TreeType {
    private static final Map<String, TreeType> cache = new ConcurrentHashMap<>();

    private final String species;
    private final String color;
    private final String texture;

    private TreeType(String species, String color, String texture) {
        this.species = species;
        this.color = color;
        this.texture = texture;
    }

    public static TreeType get(String species, String color, String texture) {
        String key = species + "|" + color + "|" + texture;
        return cache.computeIfAbsent(key, k -> new TreeType(species, color, texture));
    }

    public static int cacheSize() {
        return cache.size();
    }

    public String render(int x, int y) {
        return "Rendering " + species + " at (" + x + ", " + y + ") color=" + color;
    }
}

final class Tree {
    private final int x;
    private final int y;
    private final TreeType type;

    public Tree(int x, int y, TreeType type) {
        this.x = x;
        this.y = y;
        this.type = type;
    }

    public String render() {
        return type.render(x, y);
    }
}

public class FlyweightJava {
    public static List<Tree> buildForest(int n) {
        TreeType type = TreeType.get("Oak", "green", "bark.png");
        List<Tree> forest = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            forest.add(new Tree(i, i, type));
        }
        return forest;
    }

    public static List<Tree> buildMixedForest(int n) {
        TreeType[] types = {
            TreeType.get("Oak", "green", "bark.png"),
            TreeType.get("Pine", "dark", "pine.png"),
            TreeType.get("Birch", "light", "birch.png"),
        };
        List<Tree> forest = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            forest.add(new Tree(i, i, types[i % types.length]));
        }
        return forest;
    }

    public static void main(String[] args) {
        List<Tree> forest = buildForest(1000);
        System.out.println(forest.get(0).render());
        System.out.println(forest.get(999).render());
        System.out.println("Unique tree types: " + TreeType.cacheSize());

        List<Tree> mixed = buildMixedForest(3000);
        System.out.println("\nMixed forest: " + mixed.size() + " trees, " + TreeType.cacheSize() + " unique types");
    }
}
