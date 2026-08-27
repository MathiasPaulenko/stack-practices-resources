import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

record Event(String type) {}

public class CopyOnWriteEventDispatcher {
    private final CopyOnWriteArrayList<Consumer<Event>> listeners = new CopyOnWriteArrayList<>();

    public void addListener(Consumer<Event> listener) {
        listeners.add(listener);
    }

    public void removeListener(Consumer<Event> listener) {
        listeners.remove(listener);
    }

    public void dispatch(Event event) {
        for (Consumer<Event> listener : listeners) {
            listener.accept(event);
        }
    }

    public static void main(String[] args) {
        CopyOnWriteEventDispatcher dispatcher = new CopyOnWriteEventDispatcher();
        dispatcher.addListener(event -> System.out.println("Listener A: " + event.type()));
        dispatcher.addListener(event -> System.out.println("Listener B: " + event.type()));
        dispatcher.dispatch(new Event("user_login"));
        dispatcher.dispatch(new Event("user_logout"));
    }
}
