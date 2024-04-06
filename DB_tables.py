"""
This file defines the database tables for customers and sellers.

The DB_tables.py file defines two SQLAlchemy ORM classes: Customer_Record and Seller_Record.
These classes represent database tables 'customers' and 'sellers' respectively, and are
used to map Python objects to corresponding database tables.

- Customer_Record class maps to the 'customers' table and contains columns for customer 
  identification (id), item type (item_type), and item quantity (item_quantity).
- Seller_Record class maps to the 'sellers' table and contains columns for seller 
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

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
from config import db_string

Base = declarative_base()
engine = create_engine(db_string)

class Customer_Record(Base):
    __tablename__ = 'customers'
    id = Column(Integer)
    item_type = Column(String(30))
    item_quantity = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'item_type'),
        {'schema': 'public'}
    )

    def __repr__(self) -> str:
        return f"<customers(id={self.id}, item_type={self.item_type}, item_quantity={self.item_quantity})>"
    

class Seller_Record(Base):
    __tablename__ = 'sellers'
    id = Column(Integer)
    item_type = Column(String(30))
    item_quantity = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'item_type'),
        {'schema': 'public'}
    )

    def __repr__(self) -> str:
        return f"<sellers(id={self.id}, item_type={self.item_type}, item_quantity={self.item_quantity})>"