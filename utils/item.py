from enum import Enum


class CustomEnum(Enum):
    def __get__(self, instance, owner):
        return self.value


class ItemType(CustomEnum):
    ENGINE = "engine"
    WHEELS = "wheels"


class Item:
    def __init__(self, item_type: ItemType, quantity: int):
        self.item_type = item_type
        self.quantity = quantity

    def __lt__(self, other) -> bool:
        return self.quantity < other.quantity

    def __gt__(self, other) -> bool:
        return self.quantity > other.quantity

    def __repr__(self) -> str:
        return f"{self.item_type}: {self.quantity}"

    def __add__(self, other):
        return self.quantity + other.quantity

    def __eq__(self, other):
        return self.item_type == other.item_type
