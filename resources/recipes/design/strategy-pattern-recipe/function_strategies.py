from typing import Callable, List
from dataclasses import dataclass

@dataclass
class Order:
    items: List[float]
    total_weight: float
    destination: str

# Strategies are plain functions
Strategy = Callable[[Order], float]

def flat_rate_strategy(order: Order) -> float:
    return 10.0

def weight_based_strategy(order: Order) -> float:
    return order.total_weight * 2.5

def free_over_threshold(order: Order) -> float:
    subtotal = sum(order.items)
    return 0.0 if subtotal > 50 else 5.0

class CheckoutService:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def get_total(self, order: Order) -> float:
        subtotal = sum(order.items)
        shipping = self.strategy(order)
        return subtotal + shipping

# Runtime selection
strategies = {
    'domestic': flat_rate_strategy,
    'international': weight_based_strategy,
    'promo': free_over_threshold,
}

checkout = CheckoutService(strategies[order.destination])
total = checkout.get_total(order)
