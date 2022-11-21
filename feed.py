import streamlit as st
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.shared import JsCode
from linkedin import linkedin
import json, ast


st.set_page_config(page_title="Red State Vs Blue State", layout="wide") 
st.markdown("<h1 style='text-align: center; color: grey;'>Red State Vs Blue State</h1>", unsafe_allow_html=True)

authentication = linkedin.LinkedInDeveloperAuthentication(
                    CONSUMER_KEY,
                    CONSUMER_SECRET,
                    USER_TOKEN,
                    USER_SECRET,
                    RETURN_URL,
                    linkedin.PERMISSIONS.enums.values()
                )
application = linkedin.LinkedInApplication(authentication)
update_types = (NETWORK_UPDATES.CONNECTION, NETWORK_UPDATES.SHARED, NETWORK_UPDATES.VIRAL)
feed = application.get_network_updates(update_types)
feed = ast.literal_eval(json.dumps(feed))
df = pd.read_json(feed)


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="max", editable=True)
gb.configure_column("average net worth", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="$ ")
gridOptions = gb.build()
AgGrid(df,
              gridOptions=gridOptions,
              allow_unsafe_jscode=True, 
              fit_columns_on_grid_load=True,
              update_mode=GridUpdateMode.SELECTION_CHANGED)
