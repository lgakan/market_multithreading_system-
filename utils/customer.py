import random
from typing import List, Union

from utils.item import Item, ItemType


class Customer:
    def __init__(self, customer_id: int, shopping_list: List[Item]):
        self.customer_id = customer_id
        self.shopping_list = shopping_list
        self.shopping_cart = []
        self.shopping_delay = random.uniform(0, 2)

    def buy(self, item_type: ItemType, req_quantity: int) -> None:
        customer_item = self.find_item_by_item_type(item_type)
        if customer_item is None:
            raise Exception(f"Customer doesn't want to buy {item_type} item")
        if customer_item.quantity < req_quantity:
            raise Exception(
                f"Customer wants {customer_item.quantity} {customer_item.item_type}. It's less than {req_quantity} ")
        customer_item.quantity -= req_quantity
        if customer_item.quantity == 0:
            self.shopping_list.remove(customer_item)
        self.update_shopping_cart(item_type, req_quantity)

    def find_item_by_item_type(self, item_type: ItemType) -> Union[Item, None]:
        for item in self.shopping_list:
            if item.item_type == item_type:
                return item
        return None

    def update_shopping_cart(self, item_type: ItemType, req_quantity: int) -> None:
        for item in self.shopping_cart:
            if item_type == item.item_type:
                item.quantity += req_quantity
                return
        self.shopping_cart.append(Item(item_type, req_quantity))

    def __repr__(self) -> str:
        list_str = f"shopping list: {self.shopping_list}"
        cart_str = f"shopping cart: {self.shopping_cart}"
        return f"Customer_{self.customer_id}: {list_str} | {cart_str}"
