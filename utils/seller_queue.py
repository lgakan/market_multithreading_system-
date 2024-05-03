from typing import List, Union, Tuple
from queue import PriorityQueue

from .seller import Seller
from .item import ItemType


class SellerQueue:

    def __init__(self, item_type: ItemType, sellers: List[Seller]):
        self.item_type = item_type
        self.queue = PriorityQueue()
        for seller in sellers:
            self.queue.put((seller.storage.find_item_by_item_type(self.item_type).quantity, seller))
        self.is_free = True

    def push(self, seller: Seller):
        self.is_free = False
        self.queue.put((seller.storage.find_item_by_item_type(self.item_type).quantity, seller))
        self.is_free = True

    def pop(self):
        return self.queue.get()
