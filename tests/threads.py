from lib.database import create_db, CRUD, engine
from utils.customer import Customer
from utils.item import Item, ItemType
from utils.market import Market
from utils.seller import Seller
from typing import List
from lib.decorators.retry_decorator import retry
from lib.decorators.timing_decorator import get_time


def setup_sellers():
    seller_1 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=1_000_000)])
    return [seller_1]


def setup_seller2():
    seller_1 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=5)])
    seller_2 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=10)])
    seller_3 = Seller(1, [Item(item_type=ItemType.ENGINE, quantity=40)])
    return [seller_1, seller_2, seller_3]


def setup_customers():
    customer_1 = Customer(1, [Item(item_type=ItemType.ENGINE, quantity=3)])
    customer_2 = Customer(2, [Item(item_type=ItemType.ENGINE, quantity=15)])
    customer_3 = Customer(3, [Item(item_type=ItemType.ENGINE, quantity=30)])
    return [customer_1, customer_2, customer_3]


def find_sellers(market: Market, item: Item):
    return market.get_available_sellers(item.item_type)


@get_time
def synch_performance(market: Market, customers_list: List[Customer]):
    for customer in customers_list:
        for customer_item in customer.shopping_list:
            found_sellers = find_sellers(market, customer_item)
            for seller in found_sellers:
                sold_quantity = seller.sell(customer_item.item_type, customer_item.quantity)
                customer.buy(customer_item.item_type, sold_quantity)
                if customer_item.quantity == 0:
                    break


@get_time
def thread_performance(market: Market, customers_list: List[Customer]):
    pass


def main():
    # customers1 = setup_customers()
    # sellers1 = setup_sellers()
    # market1 = Market(sellers1)
    # synch_performance(market1, customers1)

    customers2 = setup_customers()
    sellers2 = setup_seller2()
    market2 = Market(sellers2)
    # thread_performance(market2, customers2)
    print(market2.get_calculated_sellers(ItemType.ENGINE, 15))


if __name__ == "__main__":
    main()

