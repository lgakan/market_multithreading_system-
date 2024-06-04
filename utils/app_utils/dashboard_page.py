from typing import Dict, List

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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
        print(customers.columns.values)
        fig_col1, fig_col2 = st.columns(2)
        for fig_col, df, ID in zip([fig_col1, fig_col2], [customers, sellers], ['CustomerID', 'SellerID']):
            with fig_col:
                fig = go.Figure(
                    data=[
                        go.Bar(
                            x=df[column_name].to_list(),
                            y=df[ID].to_list(),
                            orientation='h',
                            name=column_name,
                            width=0.2
                        ) for column_name in df.columns.values[1:]
                    ],
                    layout=go.Layout(
                        title=f"{ID[:-2]}s' storage plot",
                        yaxis=dict(
                            # tickmode='linear',
                            # tick0=0,
                            # dtick=1,
                            range=[-0.5, min(len(df[ID]), 1000) - 0.5],
                            fixedrange=False,
                            autorange=False
                        ),
                        height=200 + 10 * len(df.columns.values[1:]) * len(df[ID]),
                    ),
                )
                # for val in [i + 0.5 for i in range(max(df[ID]))]:
                #     fig.add_shape(
                #         type='line',
                #         x0=0,
                #         x1=max(df.iloc[:, 1:].max()),
                #         y0=val,
                #         y1=val,
                #         line=dict(
                #             color='LightGray',
                #             width=0.5,
                #             dash='dot'
                #         )
                #     )
                config = {
                    'displayModeBar': False,
                    'staticPlot': False
                }
                with st.container(height=min(400, 60 + 200 + 10 * len(df.columns.values[1:]) * len(df[ID]))):
                    st.plotly_chart(fig, use_container_width=True, config=config)


    def show_page(self, customers: pd.DataFrame, sellers: pd.DataFrame):
        st.title(self.page_name)
        options = ['Synchronous (one-threaded)', 'Asynchronous (multithreading)']
        async_options = ['Priority queue', 'List']
        option = st.radio("Choose transactions execution: ", options=options)
        if option == 'Asynchronous (multithreading)':
            async_option = st.radio("Choose structure for asynchronous system: ", options=async_options)
        else:
            async_option = None
        is_delayed = st.toggle("Simulate delays between customers' requests")
        if st.button("Start!"):
            self.show_users_data('Start Users', 'gray', customers, sellers)

            st.header('Transactions', divider='blue')
            customers_dict = customers_pd_to_dict(customers)
            sellers_dict = sellers_pd_to_dict(sellers)
            market = Market(list(sellers_dict.values()))
            if option == 'Synchronous (one-threaded)':
                market.synch_simulation(list(customers_dict.values()), is_delayed)
            elif async_option == 'Priority queue':
                market.thread_simulation(list(customers_dict.values()), is_queue=True, is_delayed=is_delayed)
            elif async_option == 'List':
                market.thread_simulation(list(customers_dict.values()), is_queue=False, is_delayed=is_delayed)
            transactions_df = create_transactions_df(market)
            st.dataframe(transactions_df, hide_index=True, use_container_width=True)

            # fig_start = go.Figure(go.Bar(
            #     x=categories,
            #     y=values,
            #     orientation='v'  # 'v' for vertical bars
            # ))

            customers_pd = customers_dict_to_pd(customers_dict, customers.columns)
            sellers_pd = sellers_dict_to_pd(sellers_dict, sellers.columns)
            self.show_users_data('End Users', 'green', customers_pd, sellers_pd)
        else:
            st.info('Click "Start!" button to run the system!')
            st.stop()
