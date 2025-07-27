import streamlit as st
from scentmatch.translator import translate

st.set_page_config(page_title=translate("app.title"), page_icon=":material/fragrance:")

page_home = st.Page("./pages/page_home.py", title=translate("app.home"), icon=":material/home:")
page_lucky = st.Page(
    "./pages/page_lucky.py", title=translate("app.feeling_lucky"), icon=":material/fragrance:"
)

pg = st.navigation([page_home, page_lucky])

pg.run()
