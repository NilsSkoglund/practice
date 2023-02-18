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

def skapa_mål_func(skapa_mål):

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
                            , "noteringar":noteringar
                            , "uppnått": False}
                add_goal_to_db(temp_dct)            

def goal_reached_update_db(item, key):
    item["uppnått"] = st.session_state[key]
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    db.put(item)


def display_goal(item):

    with st.expander(item["namn"]):
        st.markdown("---")
        st.markdown("**Beskrivning av mål:**")
        st.write(item["beskrivning"])
        st.markdown("**Datum för mål:**")
        datum = item['datum']
        datum_string = f"{datum['år']}-{datum['månad']}-{datum['dag']}"
        st.write(datum_string)
        if item["noteringar"] != "":
            st.markdown("**Övriga noteringar:**")
            st.write(item["noteringar"])
        key = item["key"] + "uppnått"
        st.checkbox("Uppnåt"
                    , value = item["uppnått"]
                    , key = key
                    , on_change=goal_reached_update_db
                    , args = (item, key))


def display_goals(kvartal):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    items = db.fetch({"kvartal": kvartal}).items

    if len(items) == 0:
        st.info(f"Inget mål har lagts till för {kvartal}")

    st.header(kvartal)

    for item in items:
        display_goal(item)

välj_kvartal = st.radio("Vilket kvartal vill du se?"
                        , ('Q1', 'Q2', 'Q3', 'Q4')
                        , horizontal=True)

display_goals(välj_kvartal)

skapa_mål = st.checkbox("Lägg till ett nytt mål")
skapa_mål_func(skapa_mål)

def ta_bort_mål(key):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    db.delete(key)

def meny_ta_bort_mål(ta_bort):
    if ta_bort:
        db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
        items = db.fetch().items

        display = "Tryck i checkbox för att ta bort målet"
        with st.expander(display, expanded = True):

            for item in items:
                display = f"{item['namn']} {item['kvartal']}"
                st.checkbox(display
                            , key = item["key"]
                            , on_change = ta_bort_mål
                            , args = (item["key"], ))

ta_bort_mål_var = st.checkbox("Ta bort mål")
meny_ta_bort_mål(ta_bort_mål_var)

