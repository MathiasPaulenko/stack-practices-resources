// Chain of Responsibility Pattern — runnable demo
// Compile & run: javac Chain.java && java Chain
abstract class Handler {
    protected Handler next;
    public Handler setNext(Handler next) { this.next = next; return next; }
    public abstract String handle(String request);
    protected String passToNext(String request) {
        if (next != null) return next.handle(request);
        return null;
    }
}
class AuthHandler extends Handler {
    public String handle(String request) {
        if (!request.startsWith("token:")) return "401 Unauthorized";
        return passToNext(request);
    }
}
class RateLimitHandler extends Handler {
    private int requests = 0;
    private final int limit = 3;
    public String handle(String request) {
        requests++;
        if (requests > limit) return "429 Too Many Requests";
        return passToNext(request);
    }
}
class DataHandler extends Handler {
    public String handle(String request) { return "Processed: " + request; }
}
public class Chain {
    public static void main(String[] args) {
        Handler handler = new AuthHandler();
        handler.setNext(new RateLimitHandler()).setNext(new DataHandler());
        System.out.println(handler.handle("token:abc"));
        System.out.println(handler.handle("bad"));
    }
}
