import pandas as pd
import streamlit as st
from st_on_hover_tabs import on_hover_tabs

from utils.app_utils.dashboard_page import DashboardPage
from utils.app_utils.data_page import DataPage
from utils.item import ItemType

if 'seller_list' not in st.session_state:
    st.session_state.seller_dict = pd.DataFrame(
        {"SellerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]})

if 'customer_dict' not in st.session_state:
    st.session_state.customer_dict = pd.DataFrame(
        {"CustomerID": [0, 1, 2], ItemType.ENGINE: [10, 0, 30], ItemType.WHEELS: [0, 20, 0]})


st.set_page_config(page_title="TMS", page_icon=":bar_chart:", layout="wide")
st.title("Threaded Market System")
st.markdown('<style>' + open('utils/app_utils/style.css').read() + '</style>', unsafe_allow_html=True)

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Customers', 'Sellers'],
                         iconName=['dashboard', 'money', 'seller'], default_choice=0)

if tabs == 'Dashboard':
    dashboard_page = DashboardPage("Dashboard")
    dashboard_page.show_page(st.session_state.customer_dict, st.session_state.seller_dict)

elif tabs == 'Customers':
    customer_page = DataPage("Customers", "CustomerID", st.session_state.customer_dict)
    st.session_state.customer_dict = customer_page.show_page()

elif tabs == 'Sellers':
    seller_page = DataPage("Sellers", "SellerID", st.session_state.seller_dict)
    st.session_state.seller_dict = seller_page.show_page()
