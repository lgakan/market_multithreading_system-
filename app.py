import copy
from datetime import datetime
from datetime import timedelta
from typing import List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from utils.seller import Seller
from utils.customer import Customer
from utils.storage import Storage
from utils.item import Item, ItemType
from st_on_hover_tabs import on_hover_tabs

#
# st.set_page_config(page_title="TMS", page_icon=":bar_chart:")
# st.title("Threaded Market System")
#
# customer_col, seller_col = st.columns(2)
# with customer_col:
#     st.write("Customers:")
#     customer_id_input, customer_add_button, customer_delete_button = st.columns(3)
#     with customer_id_input:
#         customer_id = st.number_input("Customer ID:", min_value=0, max_value=20)
#     with customer_add_button:
#         if st.button("Add new user"):
#             st.session_state.customer_list[customer_id] = Customer(customer_id, Storage())
#     with customer_delete_button:
#         if st.button("Delete chosen user"):
#             if st.session_state.customer_list.get(customer_id) is not None:
#                 st.session_state.customer_list.pop(customer_id)
#     with st.container():
#         for customer in st.session_state.customer_list.values():
#             st.write(customer)
# with seller_col:
#     st.write("Sellers:")
#     seller_id_input, seller_add_button, seller_delete_button = st.columns(3)
#     with seller_id_input:
#         seller_id = st.number_input("Seller ID:", min_value=0, max_value=20)
#     with seller_add_button:
#         if st.button("Add new seller"):
#             st.session_state.seller_list[seller_id] = Seller(seller_id, Storage())
#     with seller_delete_button:
#         if st.button("Delete chosen seller"):
#             if st.session_state.seller_list.get(seller_id) is not None:
#                 st.session_state.seller_list.pop(seller_id)
#     with st.container():
#         for seller in st.session_state.seller_list.values():
#             st.write(seller)
#
#
#
customer_1 = Customer(1, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=10)]))
customer_2 = Customer(2, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=15)]))
customer_3 = Customer(3, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=30)]))
seller_1 = Seller(1, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=5)]))
seller_2 = Seller(2, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=10)]))
seller_3 = Seller(3, Storage.inventory_from_list([Item(item_type=ItemType.ENGINE, quantity=40)]))

if 'seller_list' not in st.session_state:
    st.session_state.seller_list = {"SellerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]}

if 'customer_list' not in st.session_state:
    st.session_state.customer_list = {"CustomerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]}


def customer_page():
    df = pd.DataFrame(st.session_state.customer_list)
    df_mod = st.data_editor(df,
                            column_config={"CustomerID": st.column_config.NumberColumn("CustomerID",
                                                                                       min_value=0,
                                                                                       max_value=30,
                                                                                       default=max(df["CustomerID"]) + 1,
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


st.set_page_config(page_title="TMS", page_icon=":bar_chart:", layout="wide")
st.title("Threaded Market System")
st.markdown('<style>' + open('app/style.css').read() + '</style>', unsafe_allow_html=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Customers', 'Sellers'],
                         iconName=['dashboard', 'money', 'seller'], default_choice=1)

if tabs == 'Dashboard':
    st.title("Navigation Bar")
    if st.button("Start!"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("Start Customers")
            st.dataframe(st.session_state.customer_list, use_container_width=True)
        with col2:
            st.write("Start Sellers")
            st.dataframe(st.session_state.seller_list, use_container_width=True)
    else:
        st.info('Click "Start!" button to run the system!')
        st.stop()

elif tabs == 'Customers':
    st.title("Customers")
    customer_page()


elif tabs == 'Sellers':
    st.title("Sellers")
    seller_page()
