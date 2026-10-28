"""Fluent Builder for a Pizza object with validation and defaults."""


class Pizza:
    def __init__(self, size, cheese=False, pepperoni=False, mushrooms=False, sauce="tomato"):
        self.size = size
        self.cheese = cheese
        self.pepperoni = pepperoni
        self.mushrooms = mushrooms
        self.sauce = sauce

    def __str__(self):
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.mushrooms:
            toppings.append("mushrooms")
        return f"Pizza({self.size}, {self.sauce}, {', '.join(toppings) or 'plain'})"


class PizzaBuilder:
    def __init__(self, size="medium"):
        self.size = size
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
        self.sauce = "tomato"  # Default value

    def add_cheese(self):
        self.cheese = True
        return self

    def add_pepperoni(self):
        self.pepperoni = True
        return self

    def add_mushrooms(self):
        self.mushrooms = True
        return self

    def set_sauce(self, sauce):
        valid_sauces = ["tomato", "bbq", "pesto"]
        if sauce not in valid_sauces:
            raise ValueError(f"Invalid sauce: {sauce}. Must be one of {valid_sauces}")
        self.sauce = sauce
        return self

    def build(self):
        if not self.size:
            raise ValueError("Size is required")
        if self.size not in ["small", "medium", "large"]:
            raise ValueError(f"Invalid size: {self.size}")
        return Pizza(self.size, self.cheese, self.pepperoni, self.mushrooms, self.sauce)


if __name__ == "__main__":
    pizza = PizzaBuilder("large").add_cheese().add_pepperoni().build()
    print(pizza)  # Pizza(large, tomato, cheese, pepperoni)

    custom = PizzaBuilder("medium").add_mushrooms().set_sauce("bbq").build()
    print(custom)  # Pizza(medium, bbq, mushrooms)

    try:
        PizzaBuilder("xl").build()
    except ValueError as exc:
        print(f"Validation works: {exc}")
