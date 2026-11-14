package com.example.spotbugsdemo;

/**
 * Intentionally buggy: SpotBugs reports EI_EXPOSE_REP2 on the constructor
 * (stores a caller-owned array) and EI_EXPOSE_REP on getItems (returns the
 * internal array). Fix with defensive copies or an immutable list.
 */
public class ExposedRep {

    private final String[] items;

    public ExposedRep(String[] items) {
        this.items = items;
    }

    public String[] getItems() {
        return items;
    }
}
