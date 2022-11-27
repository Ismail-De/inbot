import streamlit as st
import pandas as pd 
import numpy as np
from lin import *


st.set_page_config(page_title="LinkedIn", layout="wide") 
st.markdown("<h1 style='text-align: center; color: grey;'>Something</h1>", unsafe_allow_html=True)

# # Show users table 
colms = st.columns((1, 2, 2, 2, 1, 1, 1, 1, 2))
fields = ["URN", 'Name', 'Title', 'Body', "Likes", "Comments", "React", "Repost", "Comment"]

cmmt = st.text_input("Your comment (by default Thanks for sharing)")

for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)

for x in feed_api():
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns((1, 2, 2, 2, 1, 1, 1, 1, 2))
    col1.write(x)
    col2.write(get_id(x))
    col3.write(get_desc_title(x)[0])
    col4.write(get_desc_title(x)[1])   # email status
    col5.write(tot_like_cmmt(x)[1])
    col6.write(tot_like_cmmt(x)[0])

    reactt = 'React'
    button_type = "React" if reactt else "Done"
    button_phold = col7.empty()
    m = x + 'r'
    do_action = button_phold.checkbox(button_type, key=m)
    if do_action:
      react(x)
      button_phold.empty()

    repostt = 'Repost'
    button_type1 = "Repost" if repostt else "Done"
    button_phold1 = col8.empty()
    m = x + 're'
    do_action1 = button_phold1.checkbox(button_type1, key=m)
    if do_action1:
      repost(x)
      button_phold1.empty()

    comment = 'Comment'
    button_type2 = "Comment" if comment else "Done"
    button_phold2 = col9.empty()
    m = x + 'c'
    do_action2 = button_phold2.checkbox(button_type2, key=m)
    if do_action2:
      if cmmt!=None:
          comment(x, message = cmmt)
      else:
         comment(x)
      button_phold2.empty()
