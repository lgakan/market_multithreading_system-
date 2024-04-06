from typing import List

from utils.item import Item


class Seller:
    def __init__(self, seller_id: int, initial_storage: List[Item]):
        self.seller_id = seller_id
        self.storage = initial_storage

    def __str__(self) -> str:
        str_storage = f"storage: {self.storage}"
        return f"Seller_{self.seller_id}:\n{str_storage}"
