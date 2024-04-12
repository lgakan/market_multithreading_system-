import random

from utils.item import Item, ItemType
from utils.storage import Storage


class Customer:
    def __init__(self, customer_id: int, initial_shopping_list: Storage):
        self.customer_id = customer_id
        self.shopping_list = initial_shopping_list
        self.shopping_cart = Storage()
        self.shopping_delay = random.uniform(0, 2)

    def buy(self, item_type: ItemType, req_quantity: int) -> None:
        customer_item = self.shopping_list.find_item_by_item_type(item_type)
        if customer_item is None:
            raise Exception(f"Customer doesn't want to buy {item_type} item")
        if customer_item.quantity < req_quantity:
            raise Exception(f"Customer wants {customer_item.quantity} {customer_item.item_type}. It's less than {req_quantity} ")
        customer_item.quantity -= req_quantity
        if customer_item.quantity == 0:
            self.shopping_list.inventory.pop(customer_item.item_type)
        self.update_shopping_cart(item_type, req_quantity)

    def update_shopping_cart(self, item_type: ItemType, req_quantity: int) -> None:
        if item_type in self.shopping_cart.inventory.keys():
            self.shopping_cart.inventory[item_type].quantity += req_quantity
        else:
            self.shopping_cart.inventory[item_type] = Item(item_type, req_quantity)

    def __repr__(self) -> str:
        list_str = f"shopping list: {self.shopping_list}"
        cart_str = f"shopping cart: {self.shopping_cart}"
        return f"Customer_{self.customer_id}: {list_str} | {cart_str}"
