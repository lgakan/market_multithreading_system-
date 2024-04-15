import random
import time
from typing import List, Dict, Union

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller
from utils.transaction import Transaction


class Market:
    def __init__(self, sellers: List[Seller] = None):
        if sellers is None:
            self.sellers = []
        else:
            self.sellers = sellers
        self.threads = []
        self.transactions: List[Transaction] = []

    def get_busy_sellers(self) -> List[Seller]:
        busy_sellers = []
        for seller in self.sellers:
            if seller.is_free is False:
                busy_sellers.append(seller)
        return busy_sellers

    def get_available_sellers(self, search_item_type: ItemType) -> List[Seller]:
        available_sellers = []
        for seller in self.sellers:
            if seller.is_free:
                seller_item = seller.storage.find_item_by_item_type(search_item_type)
                if seller_item is not None:
                    available_sellers.append(seller)
        return available_sellers

    def get_calculated_sellers(self, item_type: ItemType, target_quantity: int) -> Union[Dict[Seller, int], None]:
        available_sellers = self.get_available_sellers(item_type)
        # Sprawdzamy czy istnieje pojedynczy sprzedawca, który ma co najmniej tyle produktów ile target_quantity
        for seller in available_sellers:
            seller_item = seller.storage.find_item_by_item_type(item_type)
            if seller_item.quantity >= target_quantity:
                return {seller: min(target_quantity, seller_item.quantity)}
        # Sortujemy sprzedawców według ilości dostępnych produktów, aby rozpocząć od tych z największą ilością
        sorted_sellers = sorted(available_sellers, key=lambda x: x.storage.find_item_by_item_type(item_type).quantity, reverse=True)
        # Przechowujemy ilość produktów do kupienia od każdego sprzedawcy
        quantity_to_buy_from_sellers = {}
        # Dla każdego sprzedawcy sprawdzamy czy możemy kupić część produktów
        remaining_quantity = target_quantity
        for seller in sorted_sellers:
            seller_item_quantity = seller.storage.find_item_by_item_type(item_type).quantity
            if seller_item_quantity >= remaining_quantity:
                quantity_to_buy_from_sellers[seller] = remaining_quantity
                return quantity_to_buy_from_sellers
            elif seller_item_quantity > 0:
                quantity_to_buy_from_sellers[seller] = seller_item_quantity
                remaining_quantity -= seller_item_quantity
        return None

    def perform_transaction(self, customer: Customer):
        # Sleep tutaj symuluje przyjscia customerow o roznych porach
        time.sleep(customer.shopping_delay)
        item_type = list(customer.shopping_list.inventory.keys())[0]
        current_quantity = customer.shopping_list.find_item_by_item_type(item_type).quantity
        chosen_sellers = self.get_calculated_sellers(item_type, current_quantity)
        if chosen_sellers is None:
            print(f"Customer_{customer.customer_id} wanted {chosen_sellers}")
            time.sleep(random.uniform(0, 2))
        else:
            for seller in chosen_sellers.keys():
                seller.is_free = False
            for seller, req_quantity in chosen_sellers.items():
                sold_quantity = seller.sell(item_type, req_quantity)
                customer.buy(item_type, sold_quantity)
                new_transaction = Transaction(customer, seller, item_type, req_quantity, customer.shopping_delay)
                self.transactions.append(new_transaction)
                seller.is_free = True

    def __repr__(self):
        sellers = '\n'.join([str(seller) for seller in self.sellers])
        return f"Market sellers:\n{sellers}"
