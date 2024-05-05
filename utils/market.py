import random
import time
from typing import List, Dict, Union
import concurrent.futures

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller
from utils.transaction import Transaction
from utils.seller_queue import SellerQueue, SellerPriority
from lib.decorators.timing_decorator import get_time


class Market:
    def __init__(self, sellers: List[Seller] = None):
        if sellers is None:
            self.sellers = []
        else:
            self.sellers = sellers
        self.threads = []
        self.transactions: List[Transaction] = []
        self.seller_queues: Dict[ItemType, SellerQueue] = {}

    def get_sellers_by_item_type(self, search_item_type: ItemType) -> List[Seller]:
        return [seller for seller in self.sellers if seller.storage.find_item_by_item_type(search_item_type) is not None]

    def create_queues(self):
        for obj in ItemType:
            item_type = obj.value
            sellers_having_item_type = self.get_sellers_by_item_type(item_type)
            self.seller_queues[item_type] = SellerQueue(item_type, sellers_having_item_type)

    def get_calculated_sellers(self, item_type: ItemType, target_quantity: int) -> Union[Dict[Seller, int], None]:
        seller_queue = self.seller_queues[item_type]
        # Przechowujemy ilość produktów do kupienia od każdego sprzedawcy
        quantity_to_buy_from_sellers = {}
        remaining_quantity = target_quantity

        while remaining_quantity > 0 and seller_queue.queue:
            while not seller_queue.is_free:
                print('waiting')
            seller_priority_obj = seller_queue.pop()
            seller_item_quantity, seller = seller_priority_obj.quantity, seller_priority_obj.seller

            if seller_item_quantity > remaining_quantity:
                quantity_to_buy_from_sellers[seller] = remaining_quantity
                while not seller_queue.is_free:
                    print('waiting')
                seller_queue.push(SellerPriority(seller_item_quantity - remaining_quantity, seller))
                remaining_quantity = 0

            elif seller_item_quantity > 0:
                quantity_to_buy_from_sellers[seller] = seller_item_quantity
                remaining_quantity -= seller_item_quantity

        return quantity_to_buy_from_sellers

    def perform_transaction(self, customer: Customer):
        # Sleep tutaj symuluje przyjscia customerow o roznych porach
        time.sleep(customer.shopping_delay)
        request_dict = {
            item.item_type: item.quantity
            for item in customer.shopping_list.inventory.values()
            if item.quantity > 0
        }
        chosen_sellers_dict: Dict[ItemType, Dict[Seller, int]] = {}
        for item_type, current_quantity in request_dict.items():
            chosen_sellers = self.get_calculated_sellers(item_type, current_quantity)
            if chosen_sellers:
                chosen_sellers_dict[item_type] = chosen_sellers
        if not chosen_sellers_dict:
            print(f"Customer_{customer.customer_id} wanted {request_dict}")
        else:
            for item_type, chosen_sellers in chosen_sellers_dict.items():
                for seller, req_quantity in chosen_sellers.items():
                    while not seller.is_free:
                        print('waiting')
                    seller.is_free = False
                    sold_quantity = seller.sell(item_type, req_quantity)
                    customer.buy(item_type, sold_quantity)
                    new_transaction = Transaction(customer, seller, item_type, req_quantity, customer.shopping_delay)
                    self.transactions.append(new_transaction)
                    seller.is_free = True

    # TODO: Insert db logic
    # TODO: Solve conflicts with relationship db-customers
    @get_time
    def thread_simulation(self, customers_list: List[Customer]) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.perform_transaction, customers_list)

    # TODO: Insert db logic
    @get_time
    def synch_simulation(self, customers_list: List[Customer]) -> None:
        for customer in customers_list:
            self.perform_transaction(customer)

    def __repr__(self):
        sellers = '\n'.join([str(seller) for seller in self.sellers])
        return f"Market sellers:\n{sellers}"
