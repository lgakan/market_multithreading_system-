from lib.database import create_db, CRUD, engine
from utils.customer import Customer
from utils.item import Item, ItemType
from utils.seller import Seller
from utils.storage import Storage


def main():
    # ===========Create Seller Objects============
    seller_item4 = Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=24)])
    seller4 = Seller(4, seller_item4)
    seller_item5 = Storage.inventory_from_list([Item(item_type=ItemType.WHEELS, quantity=20)])
    seller5 = Seller(5, seller_item5)

    seller6 = Seller(seller_id=6, initial_storage=Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=18),
                                                                               Item(item_type=ItemType.ENGINE, quantity=11)]))

    # ===========Create Customer Objects============
    customer_item4 = Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=7)])
    customer4 = Customer(4, customer_item4)
    customer_item5 = Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=6)])
    customer5 = Customer(5, customer_item5)
    customer_item6 = Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=12)])
    customer6 = Customer(6, customer_item6)
    customer7 = Customer(customer_id=7, initial_shopping_list=Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=33),
                                                                                           Item(item_type=ItemType.WHEELS, quantity=10)]))
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


if __name__ == "__main__":
    create_db()
    main()
