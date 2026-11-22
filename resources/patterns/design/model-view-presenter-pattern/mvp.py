"""Model-View-Presenter: testable UI logic without a UI framework.

The View is an interface the GUI implements; the Presenter holds the logic
and talks only to that interface, so a fake view can drive it in tests.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import unittest


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository:
    """In-memory stand-in for a real datasource."""

    def __init__(self, users):
        self._users = {u.id: u for u in users}

    def find_by_id(self, user_id):
        return self._users.get(user_id)


class UserDetailView(ABC):
    """What the Presenter needs from the screen. The GUI implements this —
    in tests, a fake implements it instead."""

    @abstractmethod
    def show_loading(self): ...

    @abstractmethod
    def hide_loading(self): ...

    @abstractmethod
    def show_user(self, name, email): ...

    @abstractmethod
    def show_error(self, message): ...


class UserDetailPresenter:
    """All the logic that used to live inside the Activity/widget."""

    def __init__(self, view: UserDetailView, repository: UserRepository):
        self._view = view
        self._repository = repository

    def on_load_clicked(self, user_id):
        if user_id is None or user_id <= 0:
            self._view.show_error("Enter a valid user id")
            return
        self._view.show_loading()
        try:
            user = self._repository.find_by_id(user_id)
            if user is None:
                self._view.show_error("User not found")
            else:
                self._view.show_user(user.name, user.email)
        finally:
            self._view.hide_loading()


class FakeView(UserDetailView):
    """Records every call so tests can assert what the user would have seen."""

    def __init__(self):
        self.calls = []

    def show_loading(self):
        self.calls.append("show_loading")

    def hide_loading(self):
        self.calls.append("hide_loading")

    def show_user(self, name, email):
        self.calls.append(f"show_user:{name}:{email}")

    def show_error(self, message):
        self.calls.append(f"show_error:{message}")


class UserDetailPresenterTest(unittest.TestCase):
    def setUp(self):
        self.repo = UserRepository([User(1, "Ada", "ada@example.com")])
        self.view = FakeView()
        self.presenter = UserDetailPresenter(self.view, self.repo)

    def test_loads_and_shows_user(self):
        self.presenter.on_load_clicked(1)
        self.assertIn("show_user:Ada:ada@example.com", self.view.calls)

    def test_shows_error_for_missing_user(self):
        self.presenter.on_load_clicked(99)
        self.assertIn("show_error:User not found", self.view.calls)

    def test_validates_input_without_touching_repository(self):
        self.presenter.on_load_clicked(0)
        self.assertIn("show_error:Enter a valid user id", self.view.calls)
        self.assertNotIn("show_loading", self.view.calls)

    def test_loading_indicators_wrap_the_lookup(self):
        self.presenter.on_load_clicked(1)
        self.assertEqual(
            self.view.calls,
            ["show_loading", "show_user:Ada:ada@example.com", "hide_loading"],
        )

    def test_loading_hidden_on_error(self):
        self.presenter.on_load_clicked(99)
        self.assertEqual(self.view.calls[-1], "hide_loading")


if __name__ == "__main__":
    unittest.main(verbosity=2)
