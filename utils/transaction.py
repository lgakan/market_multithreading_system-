from random import uniform
from typing import Union

from utils.customer import Customer
from utils.item import Item
from utils.seller import Seller


# TODO: Transform this class into @dataclass
class Transaction:

    def __init__(self, customer: Customer, seller: Seller):
        self.seller = seller
        self.customer = customer
        self.item: Union[Item, None] = None
        self.execution_time: Union[int, None] = None
        self.start_delay = uniform(0, 10)

    def execute(self, item_seller, item_req: Item) -> None:
        pass
