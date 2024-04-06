from typing import List, Union

from utils.item import Item, ItemType


class Customer:
    def __init__(self, customer_id: int, shopping_list: List[Item]):
        self.customer_id = customer_id
        self.shopping_list = shopping_list
        self.shopping_cart = []

    # def process_buy(self, item_bought: Item):
    #     match_item = self.find_item_by_item_type(item_bought.item_type)
    #     self.update_shopping_cart(item_bought, match_item)

    def find_item_by_item_type(self, item_type: ItemType) -> Union[Item, None]:
        for item in self.shopping_cart:
            if item.item_type == item_type:
                return item
        return None

    def update_shopping_cart(self, item_bought: Item) -> None:
        if item_bought in self.shopping_cart:
            cart_item = self.find_item_by_item_type(item_bought.item_type)
            cart_item.quantity += item_bought.quantity
        else:
            self.shopping_cart.append(item_bought)

    def __str__(self) -> str:
        list_str = f"shopping list: {self.shopping_list}"
        cart_str = f"shopping cart: {self.shopping_cart}"
        return f"Customer_{self.customer_id}:\n{list_str}\n{cart_str}"
