from lib.customer import Customer
from lib.item import Item
from lib.market import Market
from lib.seller import Seller
from database import create_db, CRUD, engine


def main():

    #===========Create Seller Objects============
    seller_item4= [Item(item_type='Engine', quantity=24)]
    seller4= Seller(4, seller_item4)
    seller_item5 = [Item(item_type='Wheels', quantity=20)]
    seller5 = Seller(5, seller_item5)

    seller6 = Seller(seller_id=6, initial_storage=[Item(item_type="Engine", quantity=18), Item(item_type='Wheels', quantity=11)])

    #===========Create Customer Objects============
    customer_item4 = [Item(item_type='Engine', quantity=7)]
    customer4 = Customer(4, customer_item4)
    customer_item5= [Item(item_type='Engine', quantity=6)]
    customer5 = Customer(5, customer_item5)
    customer_item6 = [Item(item_type='Engine', quantity=12)]
    customer6 = Customer(6, customer_item6)
    customer7 = Customer(customer_id=7, shopping_cart=[Item(item_type='Engine', quantity=33), Item(item_type='Wheels', quantity=10)])

    #===========Create List with Customers and Sellers Objects============
    customers_objects_list = [customer4, customer5, customer6, customer7]
    sellers_objects_list = [seller4, seller5, seller6]

    #===========Create CRUD Object============
    crud = CRUD(engine=engine)
    
    #===========Create List of Customers and Sellers Objects from Excel file============
    customers = crud.create_customers_objects_from_excel()
    sellers = crud.create_sellers_objects_from_excel()

    #===========Create Customers and Sellers Records in Database============
    crud.create_customer_in_db(customers_objects_list)
    crud.create_seller_in_db(sellers_objects_list)

    #===========Append Customers objects to a list with all Customers objects============

    customers.append(customer4)
    customers.append(customer5)
    customers.append(customer6)
    customers.append(customer7)

    #===========Append Sellers objects to a list with all Sellers objects============
    print("==================")
    sellers.append(seller4)
    sellers.append(seller5)
    sellers.append(seller6)

    #===========Create Market object=================================================
    market = Market()
    
    #===========Add customers to the market==========================================
    for customer in customers:
        market.add_customer_to_market(customer)

    #===========Add sellers to the market============================================
    for seller in sellers:
        market.add_seller_to_market(seller)

    market.print_all_sellers_inventory()
    print("---------------")
    market.print_all_customers_shopping_lists()
    print("---------------")

    #===========Execute transactions for all customers in the market=================
    for customer in customers:
        market.execute_transaction(customer)
    
    print("---------------")
    market.print_all_customers_shopping_lists()
    print("---------------")
    market.print_all_sellers_inventory()

    #===========Update Customers records in the database=============================
    crud.update_customer_in_db(customers)

    #===========Update Sellers records in the database===============================
    crud.update_seller_in_db(sellers)



if __name__ == "__main__":
    create_db()
    main()
