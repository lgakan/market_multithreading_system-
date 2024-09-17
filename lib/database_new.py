from typing import Union, List, Tuple
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from lib.db_tables import Base, engine, SellerRec, CustomerRec, TransactionRec
from utils.transaction import Transaction
from utils.customer import Customer
from utils.seller import Seller

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def clear_db_tables(engine, table: str = "all") -> None:
    with session_scope() as session:
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


def create_sellers_and_customers_in_db(seller_data, customer_data) -> None:
    clear_db_tables(engine, table="all")
    with session_scope() as session:
        for data in seller_data:
            new_seller = SellerRec(**data)
            session.add(new_seller)
        for data in customer_data:
            new_customer = CustomerRec(**data)
            session.add(new_customer)


def create_customers_in_db(customer_data) -> None:
    clear_db_tables(engine, table="customers")
    with session_scope() as session:
        for data in customer_data:
            new_customer = CustomerRec(**data)
            session.add(new_customer)


def create_sellers_in_db(seller_data) -> None:
    clear_db_tables(engine, table="sellers")
    with session_scope() as session:
        for data in seller_data:
            new_seller = SellerRec(**data)
            session.add(new_seller)


def update_customer_in_db(customer: Customer) -> None:
    try:
        with session_scope() as session:
            customer_in_db = session.query(CustomerRec).filter_by(CustomerID=customer.customer_id).first()
            if customer_in_db is not None:
                for item_type in customer.shopping_list.inventory.keys():
                    if item_type in customer.shopping_cart.inventory:
                        quantity_cart = customer.shopping_cart.inventory[item_type].quantity
                        current_quantity_in_db = getattr(customer_in_db, item_type, 0)
                        new_quantity_in_db = current_quantity_in_db - quantity_cart
                        if new_quantity_in_db <= 0:
                            new_quantity_in_db = 0
                        setattr(customer_in_db, item_type, new_quantity_in_db)

    except Exception as e:
        print(f"Exception while updating customer in database: {e}")


def update_seller_in_db(seller: Seller) -> None:
    try:
        with session_scope() as session:
            seller_in_db = session.query(SellerRec).filter_by(SellerID=seller.seller_id).first()
            if seller_in_db is not None:
                new_engine_quantity_in_db = seller.storage.inventory["engine"].quantity
                seller_in_db.engine = new_engine_quantity_in_db

                new_wheels_quantity_in_db = seller.storage.inventory["wheels"].quantity
                seller_in_db.wheels = new_wheels_quantity_in_db
            else:
                print("There is no engine item type in the inventory!")
    except Exception as e:
        print(f"Exception while updating seller in database: {e}")


def create_transaction_in_db(transaction: Transaction) -> None:
    with session_scope() as session:
        customer_id = transaction.customer.customer_id
        seller_id = transaction.seller.seller_id
        item_type = transaction.item_type
        quantity = transaction.quantity
        execution_time = transaction.execution_time
        transaction_data = {
            'CustomerID': customer_id,
            'SellerID': seller_id,
            'item_type': item_type,
            'item_quantity': quantity,
            'time': execution_time
        }
        new_transaction = TransactionRec(**transaction_data)
        session.add(new_transaction)
