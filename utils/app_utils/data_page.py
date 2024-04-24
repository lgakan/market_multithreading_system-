import pandas as pd
import streamlit as st

from utils.item import ItemType


class DataPage:
    def __init__(self, page_name: str, id_column_name: str, init_df: pd.DataFrame):
        self.page_name = page_name
        self.df = init_df
        self._data_columns = [item_type.value for item_type in ItemType]
        self._id_column_name = id_column_name

    def show_page(self) -> st.data_editor:
        st.title(self.page_name)
        uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
        if uploaded_file is not None:
            df_file = pd.read_csv(uploaded_file)
            self.df = df_file

        df_config = {self._id_column_name: st.column_config.NumberColumn(self._id_column_name,
                                                                         min_value=0,
                                                                         max_value=30,
                                                                         default=max(self.df[self._id_column_name]) + 1,
                                                                         disabled=True)}
        numeric_column_config = {}
        for col_name in self._data_columns:
            numeric_column_config[col_name] = st.column_config.NumberColumn(col_name,
                                                                            min_value=0,
                                                                            max_value=30,
                                                                            default=0)
        df_config.update(numeric_column_config)
        df_mod = st.data_editor(self.df, column_config=df_config, num_rows="dynamic", use_container_width=True)
        return df_mod
