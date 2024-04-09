from typing import Union

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Transaction:
    customer: Customer
    seller: Seller
    item_type: ItemType
    quantity: int
    start_delay: float
    execution_time: Union[int, None] = field(default=None)

    def __repr__(self):
        customer_str = f"Customer_{self.customer.customer_id}"
        seller_str = f"Seller_{self.seller.seller_id}"
        return f"{customer_str} | {seller_str} -> {self.item_type}:{self.quantity}"
