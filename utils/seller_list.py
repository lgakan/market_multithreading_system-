from typing import List


from .seller import Seller
from .item import ItemType
from .seller_quantity import SellerQuantity


class SellerList:

    def __init__(self, item_type: ItemType, sellers: List[Seller]):
        self.item_type = item_type
        self.lst = sorted([
            SellerQuantity(seller.storage.find_item_by_item_type(self.item_type).quantity, seller)
            for seller in sellers if seller.storage.find_item_by_item_type(self.item_type).quantity
        ], key=lambda x: x.quantity, reverse=True)
        self.curr_id = 0
        self.have_quantity = [True for _ in range(len(self.lst))]
        self.is_free = True

    def get(self) -> SellerQuantity:
        self.is_free = False
        seller_quantity_obj = self.lst[self.curr_id]
        self.curr_id += 1
        if self.curr_id == len(self.lst):
            self.curr_id = 0
        self.is_free = True
        return seller_quantity_obj

    def zero_quantity(self):
        self.have_quantity[self.curr_id] = False
