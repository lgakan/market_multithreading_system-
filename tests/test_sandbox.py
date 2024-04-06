"""
This file is used for testing purposes.

The text_sanbox.py file is created for testing
applications, database operations, and related functionalities. It
is created to provide testing and development without
cluttering the main application file (e.g., main.py) with testing
code or potentially risky operations.

It is recommended to use this file to safely test new features,
debug code, or perform operations related to the database without
affecting the main functionality of the application.
"""

from lib.database import create_db, CRUD, engine
from utils.customer import Customer
from utils.item import Item, ItemType
from utils.market import Market
from utils.seller import Seller


def sandbox():
    # ===========Create Seller Objects============
    seller_item4 = [Item(item_type=ItemType.ENGINE, quantity=24)]
    seller4 = Seller(4, seller_item4)
    seller_item5 = [Item(item_type=ItemType.WHEELS, quantity=20)]
    seller5 = Seller(5, seller_item5)
    seller6 = Seller(seller_id=6, initial_storage=[Item(item_type=ItemType.ENGINE, quantity=18),
                                                   Item(item_type=ItemType.WHEELS, quantity=11)])

    # ===========Create Customer Objects============
    customer_item4 = [Item(item_type=ItemType.ENGINE, quantity=7)]
    customer4 = Customer(4, customer_item4)
    customer_item5 = [Item(item_type=ItemType.ENGINE, quantity=6)]
    customer5 = Customer(5, customer_item5)
    customer_item6 = [Item(item_type=ItemType.ENGINE, quantity=12)]
    customer6 = Customer(6, customer_item6)
    customer7 = Customer(customer_id=7, shopping_list=[Item(item_type=ItemType.ENGINE, quantity=33),
                                                       Item(item_type=ItemType.WHEELS, quantity=10)])

    # ===========Create List with Customers and Sellers Objects============
    customers_objects_list = [customer4, customer5, customer6, customer7]
    sellers_objects_list = [seller4, seller5, seller6]

    # ===========Create CRUD Object============
    crud = CRUD(engine=engine)

    # ===========Create List of Customers and Sellers Objects from Excel file============
    customers = crud.create_customers_objects_from_excel()
    sellers = crud.create_sellers_objects_from_excel()

    # ===========Create Customers and Sellers Records in Database============
    crud.create_customer_in_db(customers_objects_list)
    crud.create_seller_in_db(sellers_objects_list)

    # ===========Append Customers objects to a list with all Customers objects============
    customers.append(customer4)
    customers.append(customer5)
    customers.append(customer6)
    customers.append(customer7)

    # ===========Append Sellers objects to a list with all Sellers objects============
    print("==================")
    sellers.append(seller4)
    sellers.append(seller5)
    sellers.append(seller6)

    # ===============This section contains testing of CRUD operations==============
    # ===================================CREATE====================================
    # ---------------Create Customer record in database from Customer object-------
    customer8 = Customer(customer_id=8, shopping_list=[Item(item_type=ItemType.ENGINE, quantity=88),
                                                       Item(item_type=ItemType.WHEELS, quantity=88)])
    crud.create_customer_in_db(customers=customer8)
    # ---------------Create Seller record in database from Seller object-------
    seller7 = Seller(seller_id=7, initial_storage=[Item(item_type=ItemType.ENGINE, quantity=18),
                                                   Item(item_type=ItemType.WHEELS, quantity=11)])
    crud.create_seller_in_db(sellers=seller7)

    # ===================================READ=====================================
    # ---------------Read Customer record from database--------------------------
    customer_record = crud.read_customer_from_db(customer_id=8)
    if customer_record:
        print(customer_record)
    # ---------------Read Seller record from database----------------------------
    seller_record = crud.read_seller_from_db(seller_id=7)
    if seller_record:
        print(seller_record)

    # ===================================UPDATE===================================
    # ---------------Update Customer record in database---------------------------
    crud.update_customer_in_db(customer8)
    customer_record = crud.read_customer_from_db(customer_id=8)
    if customer_record:
        print(customer_record)
    # ---------------Update Seller record in database-----------------------------
    crud.update_seller_in_db(seller7)
    seller_record = crud.read_seller_from_db(seller_id=7)
    if seller_record:
        print(seller_record)

    # ===================================DELETE===================================
    # ---------------Delete Customer record from database-------------------------
    crud.delete_customer_from_db(customer_id=8)
    customer_record = crud.read_customer_from_db(customer_id=8)
    if customer_record is None:
        print("Customer with specified ID was deleted from database!")
    # ---------------Delete Seller record from database---------------------------
    crud.delete_seller_from_db(seller_id=7)
    seller_record = crud.read_seller_from_db(seller_id=7)
    if seller_record is None:
        print("Seller with specified ID was deleted from database!")
    # ===============END OF CRUD OPERATIONS TESTING SECTION===========================

    # ===============This section contains testing of Market operations===============
    # ===========Create Market object=================================================
    market = Market()
    # ===========Add customers to the market==========================================
    for customer in customers:
        market.add_customer_to_market(customer)

    # ===========Add sellers to the market============================================
    for seller in sellers:
        market.add_seller_to_market(seller)

    market.print_all_sellers_inventory()
    print("---------------")
    market.print_all_customers_shopping_lists()
    print("---------------")
    # ===========Execute transactions for all customers in the market=================
    for customer in customers:
        market.execute_transaction(customer)
    print("---------------")
    market.print_all_customers_shopping_lists()
    print("---------------")
    market.print_all_sellers_inventory()

    # ===========Update Customers records in the database=============================
    crud.update_customer_in_db(customers)

    # ===========Update Sellers records in the database===============================
    crud.update_seller_in_db(sellers)


if __name__ == "__main__":
    # ---------------Create and initialize the database-----------------------------
    create_db()
    # ---------------Run the sandbox testing script---------------------------------
    sandbox()
