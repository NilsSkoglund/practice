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

def add_comment_to_db(key, rubrik, text):
    db.put({"Rubrik":rubrik, "Comment":text}, key)
def add_comment():

    
    key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])
    items = fetch_from_db()
    keys = [i["key"] for i in items]
    while key in keys:
        key = "".join([random.choice(string.ascii_uppercase) for i in range(16)])

    with st.form("My form"):

        rubrik = st.text_input("Rubrik")
        text = st.text_area("Kommentar:")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            rubrik = rubrik.strip().title()
            add_comment_to_db(key, rubrik, text)

    

def modify_comment(key, comment):
    db.update({"Comment":comment}, key)

def display_item():

    items = fetch_from_db()
    rubriker = [item["Rubrik"] for item in items]
    unika_rubriker = set(rubriker)

    for rubrik in unika_rubriker:
        st.subheader(rubrik)
        filtered_items = list(filter(lambda person: person['Rubrik'] == rubrik, items))
        for item in filtered_items:
            st.text_area("Some value"
                        , value=item["Comment"]
                        , key=item["key"]
                        , on_change=modify_comment
                        , args=(item["key"], item["Comment"],)
                        , label_visibility="collapsed")

add_general = st.checkbox("Lägg till...")
if add_general:
    add_comment()

display_item()

## Lägg till mål
    ## Lägg till namn på mål
    ## Lägg till checkbox