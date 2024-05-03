from typing import List, Union, Tuple
import heapq

from .seller import Seller
from .item import ItemType


class Heap:

    def __init__(self, item_type: ItemType, sellers: List[Seller]):
        self.item_type = item_type
        self.heap = [(seller.storage.find_item_by_item_type(self.item_type), seller) for seller in sellers]
        heapq.heapify(self.heap)
        self.used_heap = []
        self.is_free = True
        self.last_free_index: Union[int, None] = 0

    def get_free(self) -> Union[Tuple[int, Seller], None]:
        if self.last_free_index is not None:
            node = self.heap[self.last_free_index]
            self.used_heap.append(node)
            self.last_free_index += 1
            if self.last_free_index == len(self.heap):
                self.last_free_index = None
            return node

        for node in self.used_heap:
            if node[1].is_free:
                return node
        return None

    def update_heap(self):
        for node in self.used_heap:

    def push(self, seller: Seller):
        heapq.heappush(self.heap, (seller.storage.find_item_by_item_type(self.item_type).quantity, seller))

    def pop(self):
        return heapq.heappop(self.heap)
