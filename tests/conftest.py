from typing import List, Callable

import pytest

from utils.customer import Customer
from utils.item import Item
from utils.seller import Seller
from utils.storage import Storage


@pytest.fixture(scope="function")
def generate_customers(**kwargs) -> Callable:
    def _customers(customers_items: List[List[Item]]) -> List[Customer]:
        customers_list = []
        for customer_id, customer_items in enumerate(customers_items):
            new_customer = Customer(customer_id, Storage.inventory_from_list(customer_items))
            customers_list.append(new_customer)
        return customers_list
    return _customers


@pytest.fixture(scope="function")
def generate_sellers(**kwargs) -> Callable:
    def _sellers(sellers_items: List[List[Item]]) -> List[Seller]:
        sellers_list = []
        for seller_id, seller_items in enumerate(sellers_items):
            new_seller = Seller(seller_id, Storage.inventory_from_list(seller_items))
            sellers_list.append(new_seller)
        return sellers_list
    return _sellers
