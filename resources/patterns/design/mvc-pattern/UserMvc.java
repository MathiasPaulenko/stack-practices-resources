class UserModel {
    String name;
    String email;
    UserModel(String name, String email) {
        this.name = name;
        this.email = email;
    }
}

class UserView {
    void display(UserModel user) {
        System.out.println("User: " + user.name + " (" + user.email + ")");
    }
}

class UserController {
    private final UserModel model;
    private final UserView view;
    UserController(UserModel model, UserView view) {
        this.model = model;
        this.view = view;
    }
    void updateName(String name) {
        model.name = name;
        view.display(model);
    }
}

public class UserMvc {
    public static void main(String[] args) {
        UserController controller = new UserController(
            new UserModel("Alice", "alice@example.com"),
            new UserView()
        );
        controller.updateName("Alicia");
    }
}
