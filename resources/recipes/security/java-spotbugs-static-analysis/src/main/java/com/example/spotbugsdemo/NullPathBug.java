package com.example.spotbugsdemo;

/**
 * Intentionally buggy: SpotBugs reports NP_NULL_ON_SOME_PATH on getUserName
 * because {@code user} can be null on one path and is dereferenced.
 */
public class NullPathBug {

    public String getUserName(User user) {
        return user.getName().trim();
    }

    static class User {
        private final String name;

        User(String name) {
            this.name = name;
        }

        String getName() {
            return name;
        }
    }
}
