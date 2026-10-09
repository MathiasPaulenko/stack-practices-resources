// Minimal MVC: model owns data, view renders, controller coordinates.

class UserModel {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
}

class UserView {
  display(user) {
    console.log(`User: ${user.name} (${user.email})`);
  }
}

class UserController {
  constructor(model, view) {
    this.model = model;
    this.view = view;
  }

  updateName(name) {
    this.model.name = name;
    this.view.display(this.model);
  }
}

const controller = new UserController(
  new UserModel("Alice", "alice@example.com"),
  new UserView()
);
controller.updateName("Alicia");
