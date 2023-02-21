import streamlit as st
from datetime import datetime, time
from deta import Deta
import string
import random
import time

# Connect to Deta Base
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])
table = "general"
db = st.session_state["deta"].Base(table)
def fetch_from_db():
    return db.fetch().items

# functions

def add_comment_to_db(key, text_input, text_area):
    db.put({"Rubrik":text_input, "Comment":text_area}, key)
def add_comment():

    
    key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])
    items = fetch_from_db()
    keys = [i["key"] for i in items]
    if key in keys:
        key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])

    with st.form("My form"):

        text_input = st.text_input("Rubrik")
        text_area = st.text_area("Kommentar:")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            add_comment_to_db(key, text_input, text_area)

    

def modify_comment(key, comment):
    db.update({"Comment":comment}, key)

add_general = st.checkbox("Lägg till...")
if add_general:
    add_comment()
    time.sleep(0.5)

items = fetch_from_db()

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