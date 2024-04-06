from typing import Union, List, Tuple

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from lib.db_tables import Base, engine, CustomerRecord, SellerRecord
from utils.customer import Customer
from utils.item import ItemType, Item
from utils.seller import Seller


class DataBaseFromExcel:
    def __init__(self, engine, excel_filename: str) -> None:
        self.engine = engine
        self.excel_file_df = pd.ExcelFile(excel_filename)
        self.customer_df = pd.read_excel(self.excel_file_df, 'Customer')
        self.seller_df = pd.read_excel(self.excel_file_df, 'Seller')

    def clear_db_tables(self) -> None:
        with self.engine.begin() as connection:
            connection.execute(text("DELETE FROM customers"))
            connection.execute(text("DELETE FROM sellers"))

    def upload_data_from_excel(self) -> None:
        self.customer_df.to_sql('customers', con=self.engine, if_exists='append', index=False)
        self.seller_df.to_sql('sellers', con=self.engine, if_exists='append', index=False)


    def get_customers_ids_from_excel(self) -> List[int]:
        customer_ids = self.customer_df['id'].tolist()
        return customer_ids

    def get_sellers_ids_from_excel(self) -> List[int]:
        sellers_ids = self.seller_df['id'].tolist()
        return sellers_ids

    
class CRUD:
    def __init__(self, engine) -> None:
        self.engine = engine

    def create_customer_in_db(self, customers: Union[Customer, List[Customer]]) -> None:
        if isinstance(customers, Customer):
            customers = [customers]

        for customer in customers:
            if not customer.shopping_cart:
                return None

            with self.engine.begin() as connection:
                for item in customer.shopping_cart:
                    connection.execute(
                        CustomerRecord.__table__.insert(),
                        {
                            'id': customer.customer_id,
                            'item_type': item.item_type,
                            'item_quantity': item.quantity
                        }
                    )

    # :id oznacza, ze parametr id bedzie podstawiany dynamicznie podczas wykonywania zapytania
    # zapobiega to sql injection
    def read_customer_from_db(self, customer_id: Union[int, List[int]]) -> Union[List[List[Tuple[int, str, int]]], List[Tuple[int, str, int]], None]:
        if isinstance(customer_id, int):
            customer_id = [customer_id]

        customer_records = []
        for id in customer_id:
            try:
                with self.engine.begin() as connection:
                    customer = connection.execute(
                        text("SELECT * FROM customers WHERE id = :id"),
                        {
                            'id': id
                        }
                    )
                    customer = customer.fetchall()
                
                if customer:
                    customer_records.append(customer)
                else:
                    customer_records.append(None)
            except Exception as e:
                print(f"An error occurred while trying to read customer with id {customer_id}: {e}")
                return None
        if 1 == len(customer_records):
            return customer_records[0]
        else:
            return customer_records
        
        
    def update_customer_in_db(self, customers: Union[Customer, List[Customer]]) -> None:
        if isinstance(customers, Customer):
            customers = [customers]

        for customer in customers:
            for item in customer.shopping_cart:
                query = "UPDATE customers SET"
                values = {}

                if item.item_type is not None:
                    query += " item_type = :item_type,"
                    values["item_type"] = item.item_type

                # tutaj musi byc item_quantity is not None a nie samo if item_quantity, poniewaz ten pierwszy warunek
                # sprawdzi czy wartosc ta jest poprawna dla kazdego typu tzn rozna od None
                # a if item_quantity jesli dostanie 0 to zwroci wartosc False
                if item.quantity is not None and isinstance(item.quantity, int):
                    query += " item_quantity = :item_quantity"
                    values["item_quantity"] = item.quantity

                #wykorzystuje pattern przedstawiony wyzej i na koncu zostaje przecinek to go usuwam
                query = query.rstrip(',')
                query += " WHERE id = :id AND item_type = :item_type"
                values["id"] = customer.customer_id
                values["item_type"] = item.item_type
                
                with self.engine.begin() as connection:
                    connection.execute(
                        text(query),
                        values
                    )
        
    def delete_customer_from_db(self, customer_id: Union[int, List[int]]) -> None:
        if isinstance(customer_id, int):
            customer_id = [customer_id]
        for id in customer_id:
            with self.engine.begin() as connection:
                connection.execute(
                    text("DELETE FROM customers WHERE id = :id"),
                    {
                        'id': id
                    }
                )


    def create_seller_in_db(self, sellers: Union[Seller, List[Seller]]) -> None:
        if isinstance(sellers, Seller):
            sellers = [sellers]

        for seller in sellers:
            with self.engine.begin() as connection:
                for item in seller.storage:
                    connection.execute(
                        SellerRecord.__table__.insert(),
                        {
                            'id': seller.seller_id,
                            'item_type': item.item_type,
                            'item_quantity': item.quantity
                        }
                    )

    def read_seller_from_db(self, seller_id: Union[int, List[int]]) -> Union[List[List[Tuple[int, str, int]]], List[Tuple[int, str, int]], None]:
        if isinstance(seller_id, int):
            seller_id = [seller_id]

        seller_records = []
        for id in seller_id:
            try:
                with self.engine.begin() as connection:
                    seller = connection.execute(
                        text("SELECT * FROM sellers WHERE id = :id"),
                        {
                            'id': id
                        }
                    )
                    seller = seller.fetchall()
                
                if seller:
                    seller_records.append(seller)
                else:
                    seller_records.append(None)
            except Exception as e:
                print(f"An error occurred while trying to read seller with id {seller_id}: {e}")
                return None
        if 1 == len(seller_records):
            return seller_records[0]
        else:
            return seller_records
        
  
    def update_seller_in_db(self, sellers: Union[Seller, List[Seller]]) -> None:
        if isinstance(sellers, Seller):
            sellers = [sellers]
        
        for seller in sellers:
            for item in seller.storage:
                query = "UPDATE sellers SET"
                values = {}

                if item.item_type is not None:
                    query += " item_type = :item_type,"
                    values["item_type"] = item.item_type

                if item.quantity is not None and isinstance(item.quantity, int):
                    query += " item_quantity = :item_quantity"
                    values["item_quantity"] = item.quantity

                query = query.rstrip(',')
                query += " WHERE id = :id AND item_type = :item_type"
                values["id"] = seller.seller_id
                values["item_type"] = item.item_type
                
                with self.engine.begin() as connection:
                    connection.execute(
                        text(query),
                        values
                    )

        
    def delete_seller_from_db(self, seller_id: Union[int, List[int]]) -> None:
        if isinstance(seller_id, int):
            seller_id = [seller_id]
        for id in seller_id:
            with self.engine.begin() as connection:
                connection.execute(
                    text("DELETE FROM sellers WHERE id = :id"),
                    {
                        'id': id
                    }
                )

    def find_sellers_by_item_type(self, item_type: ItemType) -> Union[List[SellerRecord], None]:
        try: 
            with self.engine.begin() as connection:
                sellers = connection.execute(
                    text("SELECT * FROM sellers WHERE item_type = :item_type"),
                    {
                        'item_type':item_type
                    }
                )
                sellers = sellers.fetchall()

            return sellers
        except Exception as e:
            print(f"An error occurred while trying to find sellers with item type {item_type} : {e}")
            return None
        
    def get_min_max_ids_from_column(self, table_name: str) -> Tuple[int, int]:
        with self.engine.begin() as connection:
            ids = connection.execute(
                text(f"SELECT MIN(id), MAX(id) FROM {table_name}")
            )
            ids = ids.fetchone()
            min_id, max_id = ids
            if min_id is None or max_id is None:
                raise IntegrityError("The 'id' column is empty.")
            return (ids[0], ids[1])
        
    def create_customers_objects_from_excel(self) -> Union[List[Customer], None]:
        min_id, max_id = self.get_min_max_ids_from_column(table_name='customers')
        customers = []
        for id in range(min_id, max_id + 1):

            customer_record = self.read_customer_from_db(id)
            for row in customer_record:
                customer_id = row[0]
                shopping_cart = [Item(item_type=row[1], quantity=row[2])]
                customer = Customer(customer_id=customer_id, shopping_cart=shopping_cart)
                customers.append(customer)
        return customers
    
    def create_sellers_objects_from_excel(self) -> Union[List[Seller], None]:

        min_id, max_id = self.get_min_max_ids_from_column(table_name='sellers')
        sellers = []
        for id in range(min_id, max_id + 1):
            seller_record = self.read_seller_from_db(id)
            for row in seller_record:
                seller_id = row[0]
                initial_storage = [Item(item_type=row[1], quantity=row[2])]
                seller = Seller(seller_id=seller_id, initial_storage=initial_storage)
                sellers.append(seller)
        return sellers


def create_db() -> None:
    Base.metadata.create_all(engine)
    database = DataBaseFromExcel(engine, 'data/Car_Selling_Excel.xlsx')
    database.clear_db_tables()
    database.upload_data_from_excel()


