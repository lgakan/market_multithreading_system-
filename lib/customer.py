from typing import List, Union

from lib.item import Item, ItemType
from lib.user import AbstractUser



class Customer(AbstractUser):
    def __init__(self, customer_id: int, shopping_list: List[Item]):
        super().__init__(customer_id)
        self.shopping_list = shopping_list
        self.shopping_cart = []

    def __str__(self) -> str:
        str_dict = super().__str__()
        return "\n".join([f"Customer_{self.user_id}'s {str_list}:\n{str_dict[str_list]}" for str_list in str_dict])

    def process_buy(self, item_bought: Item):
        match_item = self.find_item_by_item_type(item_bought.item_type, self.shopping_cart)
        self.update_shopping_cart(item_bought, match_item)

    def update_shopping_cart(self, item_bought: Item, customer_item: Union[Item, None]) -> None:
        if customer_item:
            customer_item.quantity += item_bought.quantity

        else:
            self.shopping_cart.append(item_bought.copy())
