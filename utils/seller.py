from utils.item import ItemType
from utils.storage import Storage


class Seller:
    def __init__(self, seller_id: int, initial_storage: Storage):
        self.seller_id = seller_id
        self.storage = initial_storage

    def sell(self, item_type: ItemType, req_quantity: int) -> int:
        seller_item = self.storage.find_item_by_item_type(item_type)
        if seller_item is None:
            raise Exception(f"Seller doesn't have {item_type} item")
        if seller_item.quantity < req_quantity:
            raise Exception(f"Seller has {seller_item.quantity} {seller_item.item_type} | Customer wants {req_quantity}")
        sold_quantity = min(req_quantity, seller_item.quantity)
        seller_item.quantity -= sold_quantity
        if seller_item.quantity == 0:
            self.storage.inventory.pop(seller_item.item_type)
        return sold_quantity

    def __repr__(self) -> str:
        str_storage = f"storage: {self.storage}"
        return f"Seller_{self.seller_id} {str_storage}"
