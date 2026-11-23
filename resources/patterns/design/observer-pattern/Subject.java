import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

interface Observer {
    void update(String data);
}

/**
 * Observer pattern: the subject keeps a list of observers and calls
 * update() on each one when its state changes.
 */
public class Subject {
    private final List<Observer> observers = new ArrayList<>();

    /** Subscribe and return a Runnable that unsubscribes — call it in teardown. */
    Runnable attach(Observer o) {
        observers.add(o);
        return () -> observers.remove(o);
    }

    void notifyObservers(String data) {
        for (Observer o : observers) {
            try {
                o.update(data);
            } catch (RuntimeException e) {
                // one bad observer must not break the rest
                System.err.println("Observer error: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        Subject subject = new Subject();
        subject.attach(data -> System.out.println("A received: " + data));
        Runnable unsubB = subject.attach(data -> System.out.println("B received: " + data));

        subject.notifyObservers("Hello observers!");
        unsubB.run();
        subject.notifyObservers("B is gone");
    }
}
