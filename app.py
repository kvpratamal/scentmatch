import streamlit as st

st.set_page_config(page_title="Legendary Scent Match", page_icon=":material/fragrance:")

page_home = st.Page("./pages/page_home.py", title="Home", icon=":material/home:")

pg = st.navigation([page_home])

pg.run()
