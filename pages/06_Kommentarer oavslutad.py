import streamlit as st
from datetime import datetime, time
from deta import Deta

# Connect to Deta Base
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])
table = "general"
db = st.session_state["deta"].Base(table)

# functions
def add_comment():
    db.put(st.session_state[key_add_comment])

def modify_comment(key, comment):
    db.update({"Comment":comment}, key)



temp_dct = {"Comment":""}
try:
    db.insert(temp_dct)
except:
    pass
## Lägg till Kommentar
    ## Text  area
key_add_comment = "Lägg till kommentar"
st.button(key_add_comment
            , key = f"{key_add_comment}"
            , on_click=add_comment)

items = db.fetch().items

for item in items:
    st.text_area("comment"
                , value=item["Comment"]
                , key=item["key"]
                , on_change=modify_comment
                , args=(item["key"], item["Comment"])
                , label_visibility="collapsed")

## Lägg till mål
    ## Lägg till namn på mål
    ## Lägg till checkbox