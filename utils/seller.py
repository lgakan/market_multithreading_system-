from typing import List, Union

from utils.item import Item, ItemType


class Seller:
    def __init__(self, seller_id: int, initial_storage: List[Item]):
        self.seller_id = seller_id
        self.is_free = True
        self.storage = initial_storage

    def sell(self, item_type: ItemType, req_quantity: int) -> int:
        seller_item = self.find_item_by_item_type(item_type)
        if seller_item is None:
            raise Exception(f"Seller doesn't have {item_type} item")
        if seller_item.quantity < req_quantity:
            raise Exception(f"Seller has {seller_item.quantity} {seller_item.item_type} | Customer wants {req_quantity}")
        sold_quantity = min(req_quantity, seller_item.quantity)
        seller_item.quantity -= sold_quantity
        if seller_item.quantity == 0:
            self.storage.remove(seller_item)
        return sold_quantity

    def find_item_by_item_type(self, item_type: ItemType) -> Union[Item, None]:
        for item in self.storage:
            if item.item_type == item_type:
                return item
        return None

    def __repr__(self) -> str:
        str_storage = f"storage: {self.storage}"
        return f"Seller_{self.seller_id}:\n{str_storage}"
