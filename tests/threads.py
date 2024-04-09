import concurrent.futures
import time
from typing import List

from lib.decorators.timing_decorator import get_time
from utils.customer import Customer
from utils.item import Item, ItemType
from utils.market import Market
from utils.seller import Seller


def setup_sellers1():
    seller_1 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=1_000_000)])
    return [seller_1]


def setup_seller2():
    seller_1 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=5)])
    seller_2 = Seller(2, [Item(item_type=ItemType.ENGINE, quantity=10)])
    seller_3 = Seller(3, [Item(item_type=ItemType.ENGINE, quantity=40)])
    return [seller_1, seller_2, seller_3]


def setup_customers():
    customer_1 = Customer(1, [Item(item_type=ItemType.ENGINE, quantity=10)])
    customer_2 = Customer(2, [Item(item_type=ItemType.ENGINE, quantity=15)])
    customer_3 = Customer(3, [Item(item_type=ItemType.ENGINE, quantity=30)])
    return [customer_1, customer_2, customer_3]


def find_sellers(market: Market, item: Item):
    return market.get_available_sellers(item.item_type)


# TODO: Insert db logic
@get_time
def synch_performance(market: Market, customers_list: List[Customer]):
    for customer in customers_list:
        for customer_item in customer.shopping_list:
            found_sellers = find_sellers(market, customer_item)
            for seller in found_sellers:
                time.sleep(customer.shopping_delay)
                sold_quantity = seller.sell(customer_item.item_type, customer_item.quantity)
                customer.buy(customer_item.item_type, sold_quantity)
                if customer_item.quantity == 0:
                    break


# TODO: Insert db logic
# TODO: Solve conflicts with relationship db-customers
@get_time
def thread_performance(market: Market, customers_list: List[Customer]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(market.perform_transaction, customers_list)
        print(*market.transactions, sep='\n')


def main():
    customers1 = setup_customers()
    sellers1 = setup_sellers1()
    market1 = Market(sellers1)
    print("BEFORE - customers")
    print(*customers1, sep='\n')
    print("BEFORE - Market")
    print(*market1.sellers, sep='\n')
    synch_performance(market1, customers1)
    print("AFTER - customers")
    print(*customers1, sep='\n')
    print("AFTER - Market")
    print(*market1.sellers, sep='\n')
    # ======================================
    print("\n\n\n")
    customers2 = setup_customers()
    sellers2 = setup_seller2()
    market2 = Market(sellers2)
    print("customers")
    print(*customers2, sep='\n')
    print()
    print("Market")
    print(*market2.sellers, sep='\n')
    print()
    thread_performance(market2, customers2)
    print(f"{'AFTER':^30}")
    print("customers")
    print(*customers2, sep='\n')
    print()
    print("Market")
    print(*market2.sellers, sep='\n')
    print()


if __name__ == "__main__":
    main()
