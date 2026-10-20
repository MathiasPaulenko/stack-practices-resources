package com.myapp.counter;

// Module-like unit: private state + public static API
public class Counter {
    private static int count = 0;

    private static void log(String operation) {
        System.out.println("Counter " + operation + ": " + count);
    }

    public static int increment() {
        count++;
        log("incremented");
        return count;
    }

    public static int decrement() {
        count--;
        log("decremented");
        return count;
    }

    public static int getCount() {
        return count;
    }

    public static void main(String[] args) {
        Counter.increment();
        Counter.increment();
        System.out.println(Counter.getCount()); // 2
    }
}
