from typing import Dict, List

import pandas as pd
import streamlit as st

from utils.customer import Customer
from utils.item import ItemType, Item
from utils.market import Market
from utils.seller import Seller
from utils.storage import Storage


def customers_pd_to_dict(customers_pd: pd.DataFrame) -> Dict[int, Customer]:
    customers_dict = {}
    for row_id in range(customers_pd.shape[0]):
        customer_id, engine_amount, wheels_amount = customers_pd.iloc[row_id].to_list()
        customers_dict[customer_id] = Customer(customer_id, Storage.inventory_from_list( [Item(ItemType.ENGINE, engine_amount),
                                                                                          Item(ItemType.WHEELS, wheels_amount)]))
    return customers_dict


def customers_dict_to_pd(customers_dict: Dict[int, Customer], pd_columns: List[str]) -> pd.DataFrame:
    return_pd = pd.DataFrame(columns=pd_columns)
    for customer in customers_dict.values():
        data_columns = [item_type.value for item_type in ItemType]
        new_row = [customer.customer_id]
        for col in data_columns:
            item = customer.shopping_list.inventory.get(col)
            if item is None:
                new_row.append(0)
            else:
                new_row.append(item.quantity)
        return_pd.loc[len(return_pd)] = new_row
    return return_pd


def sellers_pd_to_dict(sellers_pd: pd.DataFrame) -> Dict[int, Seller]:
    sellers_dict = {}
    for row_id in range(sellers_pd.shape[0]):
        seller_id, engine_amount, wheels_amount = sellers_pd.iloc[row_id].to_list()
        sellers_dict[seller_id] = Seller(seller_id, Storage.inventory_from_list([Item(ItemType.ENGINE, engine_amount),
                                                                                 Item(ItemType.WHEELS, wheels_amount)]))
    return sellers_dict


def sellers_dict_to_pd(sellers_dict: Dict[int, Seller], pd_columns: List[str]) -> pd.DataFrame:
    return_pd = pd.DataFrame(columns=pd_columns)
    for seller in sellers_dict.values():
        data_columns = [item_type.value for item_type in ItemType]
        new_row = [seller.seller_id]
        for col in data_columns:
            item = seller.storage.inventory.get(col)
            if item is None:
                new_row.append(0)
            else:
                new_row.append(item.quantity)
        return_pd.loc[len(return_pd)] = new_row
    return return_pd


def create_transactions_df(market: Market):
    transaction_dicts = []
    for transaction in market.transactions:
        transaction_dicts.append({
            'customerID': transaction.customer.customer_id,
            'sellerID': transaction.seller.seller_id,
            'item_type': transaction.item_type,
            'quantity': transaction.quantity})
    return pd.DataFrame(transaction_dicts)


class DashboardPage:
    def __init__(self, page_name: str):
        self.page_name = page_name

    @staticmethod
    def show_users_data(header_name: str, header_color: str, customers: pd.DataFrame, sellers: pd.DataFrame):
        st.header(header_name, divider=header_color)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Customers")
            st.dataframe(customers, hide_index=True, use_container_width=True)
        with col2:
            st.write("Sellers")
            st.dataframe(sellers, hide_index=True, use_container_width=True)

    def show_page(self, customers: pd.DataFrame, sellers: pd.DataFrame):
        st.title(self.page_name)
        if st.button("Start!"):
            self.show_users_data('Start Users', 'gray', customers, sellers)

            st.header('Transactions', divider='blue')
            customers_dict = customers_pd_to_dict(customers)
            sellers_dict = sellers_pd_to_dict(sellers)
            market = Market(list(sellers_dict.values()))
            market.create_queues()
            market.thread_simulation(list(customers_dict.values()))
            transactions_df = create_transactions_df(market)
            st.dataframe(transactions_df, hide_index=True, use_container_width=True)

            customers_pd = customers_dict_to_pd(customers_dict, customers.columns)
            sellers_pd = sellers_dict_to_pd(sellers_dict, sellers.columns)
            self.show_users_data('End Users', 'green', customers_pd, sellers_pd)
        else:
            st.info('Click "Start!" button to run the system!')
            st.stop()
