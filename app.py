import streamlit as st

st.set_page_config(page_title="Scent Match", page_icon=":material/fragrance:")

page_home = st.Page("./pages/page_home.py", title="Home", icon=":material/home:")
page_lucky = st.Page("./pages/page_lucky.py", title="Feeling Lucky", icon=":material/fragrance:")

pg = st.navigation([page_home, page_lucky])

pg.run()
