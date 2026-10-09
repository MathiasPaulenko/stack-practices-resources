"""Minimal MVC: model owns data, view renders, controller coordinates."""


class UserModel:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class UserView:
    def display(self, user: UserModel) -> None:
        print(f"User: {user.name} ({user.email})")


class UserController:
    def __init__(self, model: UserModel, view: UserView):
        self.model = model
        self.view = view

    def update_name(self, name: str) -> None:
        self.model.name = name
        self.view.display(self.model)


if __name__ == "__main__":
    controller = UserController(UserModel("Alice", "alice@example.com"), UserView())
    controller.update_name("Alicia")
