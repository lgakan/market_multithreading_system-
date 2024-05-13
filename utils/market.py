import random
import time
from typing import List, Dict, Union, Callable
import concurrent.futures

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller
from utils.transaction import Transaction
from utils.seller_queue import SellerQueue
from utils.seller_quantity import SellerQuantity
from utils.seller_list import SellerList
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
        self.seller_lists: Dict[ItemType, SellerList] = {}
        self.create_queues()
        self.create_lists()

    def create_queues(self):
        for obj in ItemType:
            item_type = obj.value
            sellers_having_item_type = self.get_sellers_by_item_type(item_type)
            self.seller_queues[item_type] = SellerQueue(item_type, sellers_having_item_type)

    def create_lists(self):
        for obj in ItemType:
            item_type = obj.value
            sellers_having_item_type = self.get_sellers_by_item_type(item_type)
            self.seller_lists[item_type] = SellerList(item_type, sellers_having_item_type)

    def get_sellers_by_item_type(self, search_item_type: ItemType) -> List[Seller]:
        return [seller for seller in self.sellers if seller.storage.find_item_by_item_type(search_item_type) is not None]

    def get_calculated_sellers_list(self, item_type: ItemType, target_quantity: int) -> Union[Dict[Seller, int], None]:
        seller_list = self.seller_lists[item_type]
        # Przechowujemy ilość produktów do kupienia od każdego sprzedawcy
        quantity_to_buy_from_sellers = {}
        remaining_quantity = target_quantity

        while remaining_quantity > 0 and any(seller_list.have_quantity):
            while not seller_list.is_free:
                print('waiting for list')
            seller_quantity_obj = seller_list.get()

            if seller_quantity_obj.quantity == 0 or seller_quantity_obj.is_busy:
                continue
            seller_quantity_obj.is_busy = True
            if seller_quantity_obj.quantity > remaining_quantity:
                quantity_to_buy_from_sellers[seller_quantity_obj.seller] = remaining_quantity
                seller_quantity_obj.quantity -= remaining_quantity
                remaining_quantity = 0

            else:
                quantity_to_buy_from_sellers[seller_quantity_obj.seller] = seller_quantity_obj.quantity
                remaining_quantity -= seller_quantity_obj.quantity
                seller_quantity_obj.quantity = 0
                seller_list.zero_quantity()

            seller_quantity_obj.is_busy = False
        return quantity_to_buy_from_sellers

    def get_calculated_sellers_queue(self, item_type: ItemType, target_quantity: int) -> Union[Dict[Seller, int], None]:
        seller_queue = self.seller_queues[item_type]
        # Przechowujemy ilość produktów do kupienia od każdego sprzedawcy
        quantity_to_buy_from_sellers = {}
        remaining_quantity = target_quantity

        while remaining_quantity > 0 and seller_queue.queue.queue:
            while not seller_queue.is_free:
                print('waiting for queue')
            seller_item_quantity, seller = seller_queue.pop()

            if seller_item_quantity > remaining_quantity:
                quantity_to_buy_from_sellers[seller] = remaining_quantity
                while not seller_queue.is_free:
                    print('waiting for queue')
                seller_queue.push(seller_item_quantity - remaining_quantity, seller)
                remaining_quantity = 0

            elif seller_item_quantity > 0:
                quantity_to_buy_from_sellers[seller] = seller_item_quantity
                remaining_quantity -= seller_item_quantity

        return quantity_to_buy_from_sellers

    def perform_transaction(self, customer: Customer, structure: str = 'list', is_delayed: bool = False) -> None:
        # Sleep tutaj symuluje przyjscia customerow o roznych porach
        if is_delayed:
            time.sleep(customer.shopping_delay)

        request_dict = {
            item.item_type: item.quantity
            for item in customer.shopping_list.inventory.values()
            if item.quantity > 0
        }
        chosen_sellers_dict: Dict[ItemType, Dict[Seller, int]] = {}
        for item_type, current_quantity in request_dict.items():
            chosen_sellers = self.get_calculated_sellers_list(item_type, current_quantity) if structure == 'list' else (
                self.get_calculated_sellers_queue(item_type, current_quantity))
            if chosen_sellers:
                chosen_sellers_dict[item_type] = chosen_sellers
        if not chosen_sellers_dict:
            print(f"Customer_{customer.customer_id} wanted {request_dict}")
        else:
            for item_type, chosen_sellers in chosen_sellers_dict.items():
                for seller, req_quantity in chosen_sellers.items():
                    while not seller.is_free:
                        print('waiting for seller')
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
