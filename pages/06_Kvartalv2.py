import streamlit as st
from datetime import datetime, time
from deta import Deta
############################## Sessuin State ###################################
if "current_date" not in st.session_state:
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

def get_goal_end_date(kvartal, år):
    if kvartal == "Q1":
        return år, 3, 31
    elif kvartal == "Q2":
        return år, 6, 30
    elif kvartal == "Q3":
        return år, 9, 30
    elif kvartal == "Q4":
        return år, 12, 31


def skapa_mål_func(skapa_mål, kvartal, år):

    if skapa_mål:
        with st.form("my_form", clear_on_submit=True):
            st.subheader("Skapa mål")
            namn = st.text_input("Namn på målet")
            beskrivning = st.text_input("Beskriv ditt mål")
            year, month, day = get_goal_end_date(kvartal, år)
            datum = st.date_input(
                "När ska målet vara uppnåt?",
                datetime(year, month, day))
            noteringar = st.text_area("Övriga anteckningar")

            submitted = st.form_submit_button("Skapa mål")

            if submitted:
                temp_dct = {"år": år
                            , "kvartal":kvartal
                            , "namn":namn
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

def display_goals(kvartal, år):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    items = db.fetch({"år": år, "kvartal": kvartal}).items

    if len(items) == 0:
        st.info(f"Finns inga mål för {kvartal} - {år}")    

    for item in items:
        display_goal(item)

def ta_bort_mål(key):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
    db.delete(key)

def meny_ta_bort_mål(ta_bort, kvartal, år):
    if ta_bort:
        db = Deta(st.secrets["deta_key"]).Base("Quarterly_goals")
        items = db.fetch({"år": år, "kvartal":kvartal}).items

        display = "Tryck i checkbox för att ta bort målet"
        with st.expander(display, expanded = True):

            for item in items:                
                st.checkbox(item['namn']
                            , key = item["key"]
                            , on_change = ta_bort_mål
                            , args = (item["key"], ))

################################# Program #####################################

with st.expander("Välj år och kvartal"):
    current_year = st.session_state["current_year"]
    lista_år = list(range(current_year, current_year+5))
    välj_år = st.radio("Vilket år vill du se?"
                            , lista_år
                            , horizontal=True)

välj_kvartal = st.radio("Vilket kvartal vill du se?"
                        , ('Q1', 'Q2', 'Q3', 'Q4')
                        , index=st.session_state["current_quarter"]
                        , horizontal=True)
st.header(f"{välj_kvartal} - {välj_år}")

vy = st.radio("Välj vy"
            , ("Visningsvy", "Redigeringsvy")
            , horizontal=True
            , label_visibility="collapsed")
            

if vy == "Redigeringsvy":

    col1, col2 = st.columns(2)

    with col1:
        skapa_mål = st.checkbox("Lägg till ett nytt mål")
    with col2:
        ta_bort_mål_var = st.checkbox("Ta bort mål")

    meny_ta_bort_mål(ta_bort_mål_var, välj_kvartal, välj_år)
    skapa_mål_func(skapa_mål, välj_kvartal, välj_år)

display_goals(välj_kvartal, välj_år)



