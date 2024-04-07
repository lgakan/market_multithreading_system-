from collections import defaultdict
from itertools import combinations
from typing import List

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

    def get_available_sellers(self, search_item_type: ItemType) -> List[Seller]:
        available_sellers = []
        for seller in self.sellers:
            if seller.is_free:
                if search_item_type in [item.item_type for item in seller.storage]:
                    available_sellers.append(seller)
        return available_sellers

    def get_calculated_sellers(self, item_type: ItemType, target_quantity: int) -> List[Seller]:
        available_sellers = self.get_available_sellers(item_type)
        # Tworzymy słownik, gdzie kluczem jest sprzedawca, a wartością jest łączna liczba produktów danego typu
        seller_items_count = defaultdict(int)
        for seller in available_sellers:
            for item in seller.storage:
                if item.item_type == item_type:
                    seller_items_count[seller] += item.quantity
        # Tworzymy kombinacje sprzedawców, aby sprawdzić możliwe zestawy, które spełniają warunek
        for i in range(1, len(available_sellers) + 1):
            for combination in combinations(available_sellers, i):
                total_quantity = sum(seller_items_count[seller] for seller in combination)
                if total_quantity >= target_quantity:
                    return list(combination)
        return []

    def perform_transaction(self, customer: Customer, item_type: ItemType, quantity: int):
        pass

    def __str__(self):
        sellers = '\n'.join([str(seller) for seller in self.sellers])
        return f"Market sellers:\n{sellers}"
