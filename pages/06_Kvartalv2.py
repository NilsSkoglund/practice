import streamlit as st
from datetime import datetime, time
from deta import Deta
############################## Sessuin State ###################################
if "end of Q1" not in st.session_state:
    st.session_state["end of Q1"] = "03-31"
    st.session_state["end of Q2"] = "06-30"
    st.session_state["end of Q2"] = "09-30"
    st.session_state["end of Q2"] = "12-31"

    st.session_state["current_date"] = datetime.now().date()
    st.session_state["current_year"] = datetime.now().date().year
    st.session_state["current_month"] = datetime.now().date().month

    st.session_state["current_quarter"] =\
         (st.session_state["current_month"]-1)//3


################################ functions ####################################
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

def skapa_mål_func(skapa_mål, kvartal):

    if skapa_mål:
        with st.form("my_form", clear_on_submit=True):
            st.subheader("Skapa mål")
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
        st.info(f"Finns inga mål för {kvartal}")    

    for item in items:
        display_goal(item)

def ta_bort_mål(key):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    db.delete(key)

def meny_ta_bort_mål(ta_bort, kvartal):
    if ta_bort:
        db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
        items = db.fetch({"kvartal":kvartal}).items

        display = "Tryck i checkbox för att ta bort målet"
        with st.expander(display, expanded = True):

            for item in items:                
                st.checkbox(item['namn']
                            , key = item["key"]
                            , on_change = ta_bort_mål
                            , args = (item["key"], ))

################################# Program #####################################

current_year = st.session_state["current_year"]
lista_år = list(range(current_year, current_year+5))
välj_år = st.radio("Vilket år vill du se?"
                        , lista_år
                        , horizontal=True)

välj_kvartal = st.radio("Vilket kvartal vill du se?"
                        , ('Q1', 'Q2', 'Q3', 'Q4')
                        , index=st.session_state["current_quarter"]
                        , horizontal=True)
st.header(välj_kvartal)

col1, col2 = st.columns(2)

with col1:
    skapa_mål = st.checkbox("Lägg till ett nytt mål")
with col2:
    ta_bort_mål_var = st.checkbox("Ta bort mål")

meny_ta_bort_mål(ta_bort_mål_var, välj_kvartal)
skapa_mål_func(skapa_mål, välj_kvartal)

display_goals(välj_kvartal)



