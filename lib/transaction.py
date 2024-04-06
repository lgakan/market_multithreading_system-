from typing import Union
from datetime import datetime

from lib.customer import Customer
from lib.item import Item
from lib.seller import Seller


class Transaction:

    def __init__(self, seller: Seller, customer: Customer):
        self.seller = seller
        self.customer = customer
        self.item_transaction: Union[Item, None] = None
        self.execution_time: Union[datetime, None] = None

    def sell(self, item_seller: Item, item_req: Item) -> Item:
        quantity_sold = min(item_seller.quantity, item_req.quantity)
        item_req.quantity -= quantity_sold
        self.item_transaction = Item(item_seller.item_type, quantity_sold)

        return self.item_transaction

    def buy(self, item_bought: Item) -> None:
        self.customer.process_buy(item_bought)

    def execute(self, item_seller, item_req: Item) -> None:
        item_bought = self.sell(item_seller, item_req)
        self.buy(item_bought)
        self.execution_time = datetime.now()
