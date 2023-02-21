import streamlit as st
from datetime import datetime, time
from deta import Deta
import string
import random

# Connect to Deta Base
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])
table = "general"
db = st.session_state["deta"].Base(table)

# functions

def add_comment_to_db(key,text_input):
    val = st.session_state[key]
    db.put({"Rubrik":text_input, "Comment":val}, key)
def add_comment():

    with st.form("My form"):
        text_input = st.text_input("Rubrik")


        key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])
        keys = [i["key"] for i in db.fetch().items]
        while key in keys:
            key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])
        text_area = st.text_area("Kommentar:"
                                , key=key
                                , on_change=add_comment_to_db
                                , args=(key, text_input))
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
    

def modify_comment(key, comment):
    db.update({"Comment":comment}, key)

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