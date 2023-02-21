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

def add_comment_to_db(key, text_input, text_area):
    db.put({"Rubrik":text_input, "Comment":text_area}, key)
def add_comment():

    form = st.form("My form")
    key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])
    keys = [i["key"] for i in db.fetch().items]
    while key in keys:
        key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])

    text_input = form.text_input("Rubrik")
    text_area = form.text_area("Kommentar:")
    # Every form must have a submit button.
    form.form_submit_button("Submit"
                        , on_click=add_comment_to_db
                        , args=(key, text_input, text_area,))
    

def modify_comment(key, comment):
    db.update({"Comment":comment}, key)

add_general = st.checkbox("Lägg till...")
if add_general:
    add_comment()

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