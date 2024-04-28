"""
This file defines the database tables for customers and sellers.

The db_tables.py file defines two SQLAlchemy ORM classes: Customer_Record and Seller_Record.
These classes represent database tables 'customers' and 'sellers' respectively, and are
used to map Python objects to corresponding database tables.

- CustomerRecord class maps to the 'customers' table and contains columns for customer
  identification (id), item type (item_type), and item quantity (item_quantity).
- SellerRecord class maps to the 'sellers' table and contains columns for seller
  identification (id), item type (item_type), and item quantity (item_quantity).

Both classes inherit from the Base class, which is imported from the database module.
The Base class serves as the declarative base for SQLAlchemy models and is used to 
define the metadata and create the actual database tables.

Each class also defines a __repr__() method, which returns a string representation of 
the object, displaying its id, item_type, and item_quantity attributes for better 
readability when debugging or inspecting objects.

These classes provide a structured and object-oriented approach to interact with 
the database tables, facilitating CRUD (Create, Read, Update, Delete) operations and 
ensuring data integrity and consistency within the application.
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

from config import db_string
import datetime

Base = declarative_base()
engine = create_engine(db_string)


# class CustomerRecord(Base):
#     __tablename__ = 'customers'
#     id = Column(Integer)
#     item_type = Column(String(30))
#     item_quantity = Column(Integer)

#     __table_args__ = (
#         PrimaryKeyConstraint('id', 'item_type'),
#         {'schema': 'public'}
#     )

#     def __repr__(self) -> str:
#         return f"<customers(id={self.id}, item_type={self.item_type}, item_quantity={self.item_quantity})>"


# class SellerRecord(Base):
#     __tablename__ = 'sellers'
#     id = Column(Integer)
#     item_type = Column(String(30))
#     item_quantity = Column(Integer)

#     __table_args__ = (
#         PrimaryKeyConstraint('id', 'item_type'),
#         {'schema': 'public'}
#     )

#     def __repr__(self) -> str:
#         return f"<sellers(id={self.id}, item_type={self.item_type}, item_quantity={self.item_quantity})>"

class SellerRec(Base):
    __tablename__ = 'sellers'
    SellerID = Column(Integer, primary_key=True)
    engine = Column(Integer)
    wheels = Column(Integer)

    __tableargs__ = (
      {'schema': 'public'}
    )

    def __repr__(self) -> str:
        return f"<sellers(id={self.SellerID}, engine={self.engine}, wheels={self.wheels})>"

class CustomerRec(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True)
    engine = Column(Integer)
    wheels = Column(Integer)

    __tableargs__ = (
      {'schema': 'public'}
    )

    def __repr__(self) -> str:
        return f"<customers(id={self.CustomerID}, engine={self.engine}, wheels={self.wheels})>"

class TransactionRec(Base):
  __tablename__= 'transactions'
  id = Column(Integer, primary_key=True, autoincrement=True)
  CustomerID = Column(Integer)
  SellerID = Column(Integer)
  item_type = Column(String(30))
  item_quantity = Column(Integer)
  time = Column(Integer)

  __tableargs__ = (
      {'schema': 'public'}
  )

  def __repr__(self) -> str:
      return f"<customer id={self.CustomerID} bought {self.item_quantity} {self.item_type} from seller id = {self.SellerID}"