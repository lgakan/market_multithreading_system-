from typing import Union

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller


# TODO: Transform this class into @dataclass
class Transaction:

    def __init__(self, customer: Customer, seller: Seller, item_type: ItemType, quantity: int, start_delay: float):
        self.customer = customer
        self.seller = seller
        self.start_delay = start_delay
        self.item_type = item_type
        self.quantity = quantity
        self.execution_time: Union[int, None] = None

    def __repr__(self):
        return f"{self.customer.customer_id} | {self.seller.seller_id} : {self.item_type}-{self.quantity}"
