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
def add_recommendation():

    
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

def display_recommendations():

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

vy = st.radio("Välj vy"
            , ("Visningsvy", "Redigeringsvy")
            , horizontal=True
            , label_visibility="collapsed")
            

if vy == "Redigeringsvy":

    col1, col2, col3 = st.columns(3)

    with col1:
        skapa_rekommendation = st.checkbox("Lägg till rekommendation")
    with col2:
        redigera_rekommentation = st.checkbox("Redigera rekommendation")
    with col3:
        ta_bort_rekommendation_var = st.checkbox("Ta bort rekommendation")

elif vy == "Visningsvy":
    display_recommendations()

if skapa_rekommendation:
    add_recommendation()
#     meny_ta_bort_mål(ta_bort_mål_var, välj_kvartal, välj_år)
#     skapa_mål_func(skapa_mål, välj_kvartal, välj_år)

# display_goals(välj_kvartal, välj_år)