/**
 * Bill Pugh holder idiom — lazy singleton with zero synchronization cost.
 *
 * The JVM initializes a class exactly once and the inner Holder class is only
 * loaded when getInstance() is first called: lazy init, thread-safe, no locks.
 */
public class Registry {
    private Registry() {
        // expensive setup would go here
    }

    private static class Holder {
        static final Registry INSTANCE = new Registry();
    }

    public static Registry getInstance() {
        return Holder.INSTANCE;
    }

    /**
     * Deserialization creates a new instance even with a private constructor.
     * readResolve() makes ObjectInputStream return the existing one instead.
     * (enum singletons get this for free.)
     */
    protected Object readResolve() {
        return getInstance();
    }

    public static void main(String[] args) {
        Registry a = Registry.getInstance();
        Registry b = Registry.getInstance();
        System.out.println("same instance: " + (a == b));
        System.out.println("identity: " + System.identityHashCode(a));
    }
}
