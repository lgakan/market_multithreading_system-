import concurrent.futures
from typing import List

import pandas as pd
import streamlit as st
from st_on_hover_tabs import on_hover_tabs

from lib.decorators.timing_decorator import get_time
from utils.customer import Customer
from utils.item import ItemType, Item
from utils.market import Market
from utils.storage import Storage
from utils.seller import Seller


if 'seller_list' not in st.session_state:
    st.session_state.seller_list = pd.DataFrame(
        {"SellerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]})

if 'customer_list' not in st.session_state:
    st.session_state.customer_list = pd.DataFrame(
        {"CustomerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]})


def setup_customers():
    customers_dict = {}
    for row_id in range(st.session_state.customer_list.shape[0]):
        customer_id, engine_amount, wheels_amount = st.session_state.customer_list.iloc[row_id].to_list()
        customers_dict[customer_id] = Customer(customer_id, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=engine_amount),
                                                          Item(item_type=ItemType.WHEELS, quantity=wheels_amount)]))
    return customers_dict


def setup_sellers():
    sellers_dict = {}
    for row_id in range(st.session_state.seller_list.shape[0]):
        seller_id, engine_amount, wheels_amount = st.session_state.seller_list.iloc[row_id].to_list()
        sellers_dict[seller_id] = Seller(seller_id, Storage.inventory_from_list([Item(ItemType.ENGINE, engine_amount),
                                                                                Item(ItemType.WHEELS, wheels_amount)]))
    return sellers_dict


def create_transactions_df(market: Market):
    transaction_dicts = []
    for transaction in market.transactions:
        transaction_dicts.append({
            'customerID': transaction.customer.customer_id,
            'sellerID': transaction.seller.seller_id,
            'item_type': transaction.item_type,
            'quantity': transaction.quantity})
    return pd.DataFrame(transaction_dicts)


def create_df_from_dict(dict_me):
    x = {"CustomerID": [], ItemType.ENGINE: [], ItemType.WHEELS: []}
    for customer in dict_me.values():
        x["CustomerID"].append(customer.customer_id)
        engine_amount = customer.shopping_list.inventory.get(ItemType.ENGINE)
        if engine_amount is None:
            x[ItemType.ENGINE].append(0)
        else:
            x[ItemType.ENGINE].append(engine_amount)
        wheels_amount = customer.shopping_list.inventory.get(ItemType.WHEELS)
        if wheels_amount is None:
            x[ItemType.WHEELS].append(0)
        else:
            x[ItemType.WHEELS].append(wheels_amount)
    return pd.DataFrame(x)




@get_time
def thread_performance(market: Market, customers_list: List[Customer]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(market.perform_transaction, customers_list)
        return results


def customer_page():
    df = pd.DataFrame(st.session_state.customer_list)
    df_mod = st.data_editor(df,
                            column_config={"CustomerID": st.column_config.NumberColumn("CustomerID",
                                                                                       min_value=0,
                                                                                       max_value=30,
                                                                                       default=max(
                                                                                           df["CustomerID"]) + 1,
                                                                                       disabled=True),
                                           ItemType.ENGINE: st.column_config.NumberColumn(ItemType.ENGINE,
                                                                                          min_value=0,
                                                                                          max_value=30,
                                                                                          default=0),
                                           ItemType.WHEELS: st.column_config.NumberColumn(ItemType.WHEELS,
                                                                                          min_value=0,
                                                                                          max_value=30,
                                                                                          default=0)},
                            num_rows="dynamic",
                            use_container_width=True)
    st.session_state.customer_list = df_mod


def seller_page():
    df = pd.DataFrame(st.session_state.seller_list)
    df_mod = st.data_editor(df,
                            column_config={"SellerID": st.column_config.NumberColumn("SellerID",
                                                                                     min_value=0,
                                                                                     max_value=30,
                                                                                     default=max(df["SellerID"]) + 1,
                                                                                     disabled=True),
                                           ItemType.ENGINE: st.column_config.NumberColumn(ItemType.ENGINE,
                                                                                          min_value=0,
                                                                                          max_value=30,
                                                                                          default=0),
                                           ItemType.WHEELS: st.column_config.NumberColumn(ItemType.WHEELS,
                                                                                          min_value=0,
                                                                                          max_value=30,
                                                                                          default=0)},
                            num_rows="dynamic",
                            use_container_width=True)
    st.session_state.seller_list = df_mod


def dashboard_page():
    if st.button("Start!"):
        st.header('Start Users ', divider='gray')
        col1, col2 = st.columns(2)
        with col1:
            st.write("Customers")
            st.dataframe(st.session_state.customer_list, hide_index=True, use_container_width=True)
        with col2:
            st.write("Sellers")
            st.dataframe(st.session_state.seller_list, hide_index=True, use_container_width=True)
        st.header('Transactions', divider='blue')
        customers = setup_customers()
        sellers = setup_sellers()
        market = Market(list(sellers.values()))
        thread_performance(market, list(customers.values()))
        transactions_df = create_transactions_df(market)
        st.dataframe(transactions_df, hide_index=True,  use_container_width=True)
        st.header('End Users', divider='green')
        col1, col2 = st.columns(2)
        with col1:
            st.write("Customers")
            st.dataframe(create_df_from_dict(customers), hide_index=True, use_container_width=True)
        with col2:
            st.write("Sellers")
            # st.dataframe(create_df_from_dict(sellers))

    else:
        st.info('Click "Start!" button to run the system!')
        st.stop()


st.set_page_config(page_title="TMS", page_icon=":bar_chart:", layout="wide")
st.title("Threaded Market System")
st.markdown('<style>' + open('app/style.css').read() + '</style>', unsafe_allow_html=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Customers', 'Sellers'],
                         iconName=['dashboard', 'money', 'seller'], default_choice=0)

if tabs == 'Dashboard':
    st.title("Dashboard")
    dashboard_page()

elif tabs == 'Customers':
    st.title("Customers")
    customer_page()


elif tabs == 'Sellers':
    st.title("Sellers")
    seller_page()
