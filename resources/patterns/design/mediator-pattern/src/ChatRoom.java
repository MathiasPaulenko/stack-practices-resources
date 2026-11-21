// Mediator pattern: chat room. Compile: javac ChatRoom.java && java ChatRoom
import java.util.ArrayList;
import java.util.List;

interface ChatMediator {
    void sendMessage(String message, User sender);
    void addUser(User user);
}

class User {
    private final String name;
    private final ChatMediator mediator;

    public User(String name, ChatMediator mediator) {
        this.name = name;
        this.mediator = mediator;
        mediator.addUser(this);
    }

    public String getName() { return name; }

    public void send(String message) {
        System.out.println(name + " sends: " + message);
        mediator.sendMessage(message, this);
    }

    public void receive(String message, String fromName) {
        System.out.println(name + " receives from " + fromName + ": " + message);
    }
}

public class ChatRoom implements ChatMediator {
    private final List<User> users = new ArrayList<>();

    public void addUser(User user) {
        users.add(user);
    }

    public void sendMessage(String message, User sender) {
        for (User user : users) {
            if (user != sender) {
                user.receive(message, sender.getName());
            }
        }
    }

    public static void main(String[] args) {
        ChatRoom room = new ChatRoom();
        User alice = new User("Alice", room);
        new User("Bob", room);
        alice.send("Hello everyone!");
    }
}
