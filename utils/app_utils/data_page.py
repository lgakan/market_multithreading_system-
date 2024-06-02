# import pandas as pd
# import streamlit as st

# from utils.item import ItemType


# class DataPage:
#     def __init__(self, page_name: str, id_column_name: str, init_df: pd.DataFrame):
#         self.page_name = page_name
#         self.df = init_df
#         self._data_columns = [item_type.value for item_type in ItemType]
#         self._id_column_name = id_column_name

#     def show_page(self) -> st.data_editor:
#         st.title(self.page_name)
#         if self.page_name == "Customers":
#             uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key=f"{self.page_name}_key")
#             if uploaded_file is not None:
#                 df_file_cust = pd.read_csv(uploaded_file)
#                 self.df = df_file_cust

#         elif self.page_name == "Sellers":
#             uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key=f"{self.page_name}_key")
#             if uploaded_file is not None:
#                 df_file_sellers = pd.read_csv(uploaded_file)
#                 self.df = df_file_sellers
#         else:
#             pass

#         # Synchronize the dataframe with session_state
#         if f'{self.page_name}_df' not in st.session_state:
#             st.session_state[f'{self.page_name}_df'] = self.df.copy()


#         df_config = {self._id_column_name: st.column_config.NumberColumn(self._id_column_name,
#                                                                          min_value=0,
#                                                                          max_value=30,
#                                                                          default=max(self.df[self._id_column_name]) + 1,
#                                                                          disabled=True)}
#         numeric_column_config = {}
#         for col_name in self._data_columns:
#             numeric_column_config[col_name] = st.column_config.NumberColumn(col_name,
#                                                                             min_value=0,
#                                                                             max_value=30,
#                                                                             default=0)
#         df_config.update(numeric_column_config)

#         df_mod = st.data_editor(st.session_state[f'{self.page_name}_df'], column_config=df_config, num_rows="dynamic", use_container_width=True)

#         if not df_mod.equals(st.session_state[f'{self.page_name}_df']):
#             st.session_state[f'{self.page_name}_df'] = df_mod

#         if st.button("Add new row"):
#             new_row = {col: 0 for col in self._data_columns}
#             new_row[self._id_column_name] = max(st.session_state[f'{self.page_name}_df'][self._id_column_name]) + 1 if not st.session_state[f'{self.page_name}_df'].empty else 0
#             new_row_df = pd.DataFrame([new_row])
#             st.session_state[f'{self.page_name}_df'] = pd.concat([st.session_state[f'{self.page_name}_df'], new_row_df], ignore_index=True)
#             #st.rerun()

#         return st.session_state[f'{self.page_name}_df']
import pandas as pd
import streamlit as st
from utils.item import ItemType

class DataPage:
    def __init__(self, page_name: str, id_column_name: str, init_df: pd.DataFrame):
        self.page_name = page_name
        self.df = init_df
        self._data_columns = [item_type.value for item_type in ItemType]
        self._id_column_name = id_column_name

    def show_page(self) -> pd.DataFrame:
        st.title(self.page_name)
        if self.page_name in ["Customers", "Sellers"]:
            uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key=f"{self.page_name}_file_uploader")
            if uploaded_file is not None:
                self.df = pd.read_csv(uploaded_file)

        # Synchronize the dataframe with session_state
        if f'{self.page_name}_df' not in st.session_state:
            st.session_state[f'{self.page_name}_df'] = self.df.copy()

        df_config = {
            self._id_column_name: st.column_config.NumberColumn(
                self._id_column_name,
                min_value=0,
                max_value=30,
                default=max(self.df[self._id_column_name]) + 1 if not self.df.empty else 0,
                disabled=True
            )
        }
        numeric_column_config = {
            col_name: st.column_config.NumberColumn(
                col_name,
                min_value=0,
                max_value=30,
                default=0
            ) for col_name in self._data_columns
        }
        df_config.update(numeric_column_config)

        df_mod = st.data_editor(st.session_state[f'{self.page_name}_df'], column_config=df_config, num_rows="dynamic", use_container_width=True)

        if not df_mod.equals(st.session_state[f'{self.page_name}_df']):
            st.session_state[f'{self.page_name}_df'] = df_mod


        if st.button("Add new row"):
            new_row = {col: 0 for col in self._data_columns}
            new_row[self._id_column_name] = max(st.session_state[f'{self.page_name}_df'][self._id_column_name]) + 1 if not st.session_state[f'{self.page_name}_df'].empty else 0
            new_row_df = pd.DataFrame([new_row])
            st.session_state[f'{self.page_name}_df'] = pd.concat([st.session_state[f'{self.page_name}_df'], new_row_df], ignore_index=True)
            st.rerun()

        return st.session_state[f'{self.page_name}_df']
