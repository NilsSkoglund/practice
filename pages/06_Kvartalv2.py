import streamlit as st
from datetime import datetime, time
from deta import Deta

def add_goal_to_db(dct):
    # Connect to Deta Base
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    namn = dct["namn"]
    kvartal = dct["kvartal"]
    key = kvartal+namn
    
    try:
        db.insert(dct, key)
    except:
        st.error(f"Mål med namn {namn} finns redan för {kvartal}")

def skapa_mål_func():
    skapa_mål = st.checkbox("Lägg till ett nytt mål")

    if skapa_mål:
        with st.form("my_form", clear_on_submit=True):
            st.subheader("Skapa mål")
            kvartal = st.radio(
                    "För vilket kvartal gäller målet?"
                    , ('Q1', 'Q2', 'Q3', 'Q4')
                    , horizontal=True)
            namn = st.text_input("Namn på målet")
            beskrivning = st.text_input("Beskriv ditt mål")
            datum = st.date_input("När ska målet vara uppnåt?")
            noteringar = st.text_area("Övriga anteckningar")

            submitted = st.form_submit_button("Skapa mål")

            if submitted:
                temp_dct = {"namn":namn
                            , "kvartal":kvartal
                            , "beskrivning":beskrivning
                            , "datum": {"år": datum.year
                                , "månad":datum.month
                                , "dag":datum.day}
                            , "noteringar":noteringar}
                add_goal_to_db(temp_dct)            


skapa_mål_func()


def display_goal(item):

    with st.expander(item["namn"]):
        st.write(item["beskrivning"])
        st.write(item["datum"])
        st.write(item["noteringar"])


def display_goals():
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")

    items = db.fetch().items

    q1 = [item for item in items if item["kvartal"] == "Q1"]

    st.write(q1)

    for item in q1:
        display_goal(item)

display_goals()
