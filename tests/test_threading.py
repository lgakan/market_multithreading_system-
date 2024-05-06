from collections import defaultdict
from typing import List, Dict

import pytest

from utils.customer import Customer
from utils.item import Item, ItemType
from utils.market import Market
from utils.seller import Seller


def check_customers(customers_list: List[Customer], sum_list: Dict[ItemType, int], sum_cart: Dict[ItemType, int]) -> None:
    customer_shopping_list = defaultdict(int)
    customer_shopping_cart = defaultdict(int)
    for customer in customers_list:
        for item in customer.shopping_list.inventory.values():
            customer_shopping_list[item.item_type] += item.quantity
        for item in customer.shopping_cart.inventory.values():
            customer_shopping_cart[item.item_type] += item.quantity

    for item_type in ItemType:

        assert customer_shopping_list.get(item_type.value, 0) == sum_list.get(item_type.value, 0), \
            f"Wrong value for {item_type} in shopping_list"

        assert customer_shopping_cart.get(item_type.value, 0) == sum_cart.get(item_type.value, 0), \
            f"Wrong value for {item_type} in shopping_cart"


def check_sellers(sellers_list: List[Seller], sum_storage: Dict[ItemType, int]) -> None:
    seller_storage = defaultdict(int)
    for seller in sellers_list:
        for item in seller.storage.inventory.values():
            seller_storage[item.item_type] += item.quantity

    for item_type in ItemType:
        assert seller_storage.get(item_type.value, 0) == sum_storage.get(item_type.value, 0), \
            f"Wrong value for {item_type} in seller storage"


class TestTreading:
    """
    The aim of this test class is to verify whether the multithreading system in the application
    will function correctly with the provided input data.
    The tests are divided into 2 main categories.
    a) When a single/multiple sellers have enough/not enough products to fulfill all orders.
    b) When a single/multiple customers want to buy fewer/more products than are available.
    In tests more means that the sellers have more items than customers want to purchase
    """

    def test_single_customer_single_seller_more(self, generate_customers, generate_sellers):
        customers_items = [[Item(ItemType.ENGINE, 10)]]
        sellers_items = [[Item(ItemType.ENGINE, 20)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 0}, {ItemType.ENGINE: 10})
        check_sellers(sellers, {ItemType.ENGINE: 10})

    def test_single_customer_single_seller_less(self, generate_customers, generate_sellers):
        customers_items = [[Item(ItemType.ENGINE, 20)]]
        sellers_items = [[Item(ItemType.ENGINE, 10)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 10}, {ItemType.ENGINE: 10})
        check_sellers(sellers, {ItemType.ENGINE: 0})

    def test_single_customer_single_seller_equal(self, generate_customers, generate_sellers):
        customers_items = [[Item(ItemType.ENGINE, 20)]]
        sellers_items = [[Item(ItemType.ENGINE, 20)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 0}, {ItemType.ENGINE: 20})
        check_sellers(sellers, {ItemType.ENGINE: 0})

    @pytest.mark.parametrize("customer_engine_quantity", [10, 20, 30, 40])
    def test_single_customer_multi_seller_more(self, generate_customers, generate_sellers, customer_engine_quantity):
        customers_items = [[Item(ItemType.ENGINE, customer_engine_quantity)]]
        sellers_items = [[Item(ItemType.ENGINE, 15)], [Item(ItemType.ENGINE, 25)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 0}, {ItemType.ENGINE: customer_engine_quantity})
        check_sellers(sellers, {ItemType.ENGINE: 40 - customer_engine_quantity})

    def test_single_customer_multi_seller_less(self, generate_customers, generate_sellers):
        customers_items = [[Item(ItemType.ENGINE, 40)]]
        sellers_items = [[Item(ItemType.ENGINE, 10)], [Item(ItemType.ENGINE, 20)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 10}, {ItemType.ENGINE: 30})
        check_sellers(sellers, {ItemType.ENGINE: 0})

    def test_multi_customer_single_seller_more(self, generate_customers, generate_sellers):
        customers_items = [[Item(ItemType.ENGINE, 15)], [Item(ItemType.ENGINE, 25)]]
        sellers_items = [[Item(ItemType.ENGINE, 50)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 0}, {ItemType.ENGINE: 40})
        check_sellers(sellers, {ItemType.ENGINE: 10})

    @pytest.mark.parametrize("seller_engine_quantity", [10, 20, 30, 40])
    def test_multi_customer_single_seller_less(self, generate_customers, generate_sellers, seller_engine_quantity):
        customers_items = [[Item(ItemType.ENGINE, 15)], [Item(ItemType.ENGINE, 25)]]
        sellers_items = [[Item(ItemType.ENGINE, seller_engine_quantity)]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: 40 - seller_engine_quantity}, {ItemType.ENGINE: seller_engine_quantity})
        check_sellers(sellers, {ItemType.ENGINE: 0})

    @pytest.mark.parametrize('seller_engine_quantity, customer_engine_quantity',
                             [((10, 20), (15, 30)),
                              ((15, 30), (10, 20)),
                              ((20, 30), (10, 40))])
    def test_multi_customer_multi_seller(self, generate_customers, generate_sellers, customer_engine_quantity, seller_engine_quantity):
        customers_items = [[Item(ItemType.ENGINE, customer_engine_quantity[0])], [Item(ItemType.ENGINE, customer_engine_quantity[1])]]
        sellers_items = [[Item(ItemType.ENGINE, seller_engine_quantity[0])], [Item(ItemType.ENGINE, seller_engine_quantity[1])]]
        customers = generate_customers(customers_items)
        sellers = generate_sellers(sellers_items)

        c_engine = sum(customer_engine_quantity)
        s_engine = sum(seller_engine_quantity)
        market = Market(sellers)
        market.thread_simulation(customers)
        check_customers(customers, {ItemType.ENGINE: max(0, c_engine-s_engine)}, {ItemType.ENGINE: min(c_engine, s_engine)})
        check_sellers(sellers, {ItemType.ENGINE: max(0, s_engine-c_engine)})
