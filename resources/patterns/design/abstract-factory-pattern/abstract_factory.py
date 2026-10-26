# Abstract Factory in Python: UI product families with a runtime registry.
from abc import ABC, abstractmethod
from typing import Dict, Type


class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class LightButton(Button):
    def render(self) -> str:
        return "Light Button"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "Light Checkbox"


class DarkButton(Button):
    def render(self) -> str:
        return "Dark Button"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "Dark Checkbox"


class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


class LightUIFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkUIFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


class FactoryRegistry:
    _factories: Dict[str, Type[UIFactory]] = {}

    @classmethod
    def register(cls, name: str, factory_class: Type[UIFactory]):
        cls._factories[name] = factory_class

    @classmethod
    def get_factory(cls, name: str) -> UIFactory:
        factory_class = cls._factories.get(name)
        if not factory_class:
            raise ValueError(f"Unknown factory: {name}")
        return factory_class()


if __name__ == "__main__":
    FactoryRegistry.register('light', LightUIFactory)
    FactoryRegistry.register('dark', DarkUIFactory)

    theme = 'dark'  # Could come from config
    factory = FactoryRegistry.get_factory(theme)
    print(factory.create_button().render())
    print(factory.create_checkbox().render())
