from typing import Union, List, Tuple

from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from lib.db_tables import Base, engine, SellerRec, CustomerRec, TransactionRec
from utils.transaction import Transaction
from utils.customer import Customer
from utils.seller import Seller

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def clear_db_tables(engine, session, table: str = "all") -> None:
    if table == "all":
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM customers"))
            connection.execute(text("DELETE FROM sellers"))
            connection.execute(text("DELETE FROM transactions"))
    elif table == "customers":
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM customers"))
    elif table == "sellers":
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM sellers"))
    elif table == "transactions":
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM transactions"))
    session.commit()
    

def create_sellers_and_customers_in_db(seller_data, customer_data) -> None:
    clear_db_tables(engine, session, table="all")
    for data in seller_data:
        new_seller = SellerRec(**data)
        session.add(new_seller)

    for data in customer_data:
        new_customer = CustomerRec(**data)
        session.add(new_customer)

    session.commit()

def create_customers_in_db(customer_data) -> None:
    clear_db_tables(engine, session, table="customers")
    for data in customer_data:
        new_customer = CustomerRec(**data)
        session.add(new_customer)
    session.commit()

def create_sellers_in_db(seller_data) -> None:
    clear_db_tables(engine, session, table="sellers")
    for data in seller_data:
        new_seller = SellerRec(**data)
        session.add(new_seller)
    session.commit()


def update_customer_in_db(customer: Customer) -> None:
    try:
        customer_in_db = session.query(CustomerRec).filter_by(CustomerID=customer.customer_id).first()
        if customer_in_db is not None:
            engine_quantity_cart = customer.shopping_cart.inventory["engine"].quantity
            current_engine_quantity_in_db = customer_in_db.engine
            new_engine_quanity_in_db = current_engine_quantity_in_db - engine_quantity_cart
            customer_in_db.engine = new_engine_quanity_in_db

            # uncomment when transactions will be performed for wheels
            # wheels_quantity_cart = customer.shopping_cart.inventory["wheels"].quantity
            # current_wheels_quantity_in_db = customer_in_db.wheels
            # new_wheels_quanity_in_db = current_wheels_quantity_in_db - wheels_quantity_cart
            # customer_in_db.wheels = new_wheels_quanity_in_db

            session.commit()
    except Exception as e:
        print(f"There was an error while updating customer in database: {e}")



def update_seller_in_db(seller: Seller) -> None:
    try:
        seller_in_db = session.query(SellerRec).filter_by(SellerID=seller.seller_id).first()
        if seller_in_db is not None:
            new_engine_quantity_in_db = seller.storage.inventory["engine"].quantity
            seller_in_db.engine = new_engine_quantity_in_db
            
            new_wheels_quantity_in_db = seller.storage.inventory["wheels"].quantity
            seller_in_db.wheels = new_wheels_quantity_in_db
            session.commit()
        else:
            print("There is no engine item type in the inventory!")

    except Exception as e:
        seller_in_db.engine = 0
        session.commit()


def create_transaction_in_db(transaction: Transaction) -> None:
    customer_id = transaction.customer.customer_id
    seller_id = transaction.seller.seller_id
    item_type = transaction.item_type
    quantity = transaction.quantity
    execution_time = transaction.execution_time
    transaction_data = {
                            'CustomerID': customer_id, 
                            'SellerID': seller_id, 
                            'item_type' : item_type, 
                            'item_quantity': quantity,
                            'time' : execution_time
                        }
    new_transaction = TransactionRec(**transaction_data)
    session.add(new_transaction)
    session.commit()