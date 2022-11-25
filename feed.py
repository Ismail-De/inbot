import streamlit as st
import pandas as pd 
import numpy as np
from lin import *


st.set_page_config(page_title="LinkedIn", layout="wide") 
st.markdown("<h1 style='text-align: center; color: grey;'>Something</h1>", unsafe_allow_html=True)

# # Show users table 
colms = st.columns((1, 2, 2, 2, 1, 1, 1, 1))
fields = ["URN", 'Name', 'Title', 'Body', "Likes", "Comments", "React", "Repost"]

for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)
def princip():
    for x in feed_api():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1, 2, 2, 2, 1, 1, 1, 1))
        col1.write(x)
        col2.write(get_id(x))
        col3.write(get_desc_title(x)[0])
        col4.write(get_desc_title(x)[1])   # email status
        col5.write(tot_like_cmmt(x)[1])
        col6.write(tot_like_cmmt(x)[0])
        reactt = 'React'
        button_type = "React" if reactt else "Done"
        button_phold = col7.empty() 
        do_action = button_phold.button(button_type, key=x)
        if do_action:
          react(x)
          reactt = ''
          button_phold.empty()
        repostt = 'Repost'
        button_type1 = "Repost" if repostt else "Done"
        button_phold1 = col8.empty()
        do_action1 = button_phold1.button(button_type1, key=x)
        if do_action:
          repost(x)
          repostt = ''
          button_phold1.empty()
bb = st.button('Start', on_click = princip())
