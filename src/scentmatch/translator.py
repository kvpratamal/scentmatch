import json
import streamlit as st

def translate(key, **kwargs):
    lang = st.session_state.get("lang", "en")
    with open(f"./locales/{lang}.json", encoding="utf-8") as f:
        translations = json.load(f)
    
    keys = key.split('.')
    value = translations
    for k in keys:
        value = value[k]

    return value.format(**kwargs)
