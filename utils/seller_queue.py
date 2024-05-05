from typing import List, Union, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field

from .seller import Seller
from .item import ItemType


@dataclass(order=True)
class SellerPriority:
    quantity: int
    seller: Seller = field(compare=False)


class SellerQueue:

    def __init__(self, item_type: ItemType, sellers: List[Seller]):
        self.item_type = item_type
        self.queue = PriorityQueue()
        for seller in sellers:
            item_quantity = seller.storage.find_item_by_item_type(self.item_type).quantity
            if item_quantity:
                self.queue.put(SellerPriority(item_quantity, seller))
        self.is_free = True

    def push(self, new_item_quantity: int, seller: Seller):
        self.is_free = False
        self.queue.put(SellerPriority(new_item_quantity, seller))
        self.is_free = True

    def pop(self):
        return self.queue.get()
