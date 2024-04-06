from typing import List, Union

from lib.item import Item
from lib.user import AbstractUser


class Seller(AbstractUser):
    def __init__(self, seller_id: int, initial_storage: List[Item]):
        super().__init__(seller_id)
        self.storage = initial_storage

    def __str__(self) -> str:
        str_dict = super().str(self)
        print(str_dict)
        return f"Seller_{self.user_id}'s storage:\n{str_dict['storage']}"
