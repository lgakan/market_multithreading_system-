from typing import List, Generator

from utils.customer import Customer
from utils.item import ItemType
from utils.seller import Seller


class Market:
    def __init__(self, sellers: List[Seller] = None):
        if sellers is None:
            self.sellers = []
        else:
            self.sellers = sellers
        self.customers: List[Customer] = []
        self.transactions: List = []

    def add_customer_to_market(self, customer: Customer) -> None:
        self.customers.append(customer)

    def remove_customer_from_market(self, customer: Customer) -> None:
        self.customers.remove(customer)

    def add_seller_to_market(self, seller: Seller) -> None:
        self.sellers.append(seller)

    def remove_seller_from_market(self, seller: Seller) -> None:
        self.sellers.remove(seller)

    def check_item_availability_on_market(self, item_type: ItemType) -> bool:
        return any(filter(lambda seller: seller.storage.item.item_type == item_type, self.sellers))
            
    def print_all_sellers_inventory(self) -> None:
        for seller in self.sellers:
            print(seller)

    def print_all_customers_shopping_lists(self) -> None:
        for customer in self.customers:
            print(customer)

    def find_seller_with_items(self, item_type: ItemType) -> Generator[Seller, None, None]:
        for seller in self.sellers:

            if any(item.item_type == item_type for item in seller.storage):
                yield seller

    """
    Currently, the execute_transaction function contains three nested declarations, 
    because I wanted to check whether executing transactions would affect records in the database. 
    The code below exists in this form for testing purposes, and a refactoring of the code 
    is needed later in the development of the project.
    """
    def execute_transaction(self, customer: Customer) -> None:
        transaction_no = 1
        if customer not in self.customers:
            return None

        print("-----------------------")
        transaction_no = 1

        for customer_req_item in customer.shopping_list:

            for potential_seller in self.find_seller_with_items(customer_req_item.item_type):

                match_item = potential_seller.find_item_by_item_type(customer_req_item.item_type, potential_seller.storage)

                if match_item.quantity == 0:
                    continue
                print(f"Transaction number {transaction_no}, customerID: {customer.customer_id} bought xxx SellerID: {potential_seller.user_id}")
                transaction_no += 1
                
                if customer_req_item.quantity == 0:
                    break
        print("-----------------------")
