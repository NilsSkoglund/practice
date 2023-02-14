import streamlit as st
from datetime import datetime
from deta import Deta

def list_week_days():
    lista_veckodagar = [
        "måndag"
        , "tisdag"
        , "onsdag"
        , "torsdag"
        , "fredag"
        , "lördag"
        , "söndag"
    ]
    for i in lista_veckodagar:
        st.checkbox(
            f"Lägg till pass {i}"
            , key = f"Vecka {week_from_input} {i}"
        )

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

st.session_state["current_week"] =\
     datetime.now().date().isocalendar().week
current_weak = st.session_state["current_week"]

st.subheader(f"Veckonummer: {current_weak}")


# Skapa träningsvecka
st.date_input(
    "Veckostart"
    , datetime.date(datetime.now())
    , key = "first_day_of_week"
)



st.session_state["week_from_input"] =\
     st.session_state["first_day_of_week"].isocalendar().week
week_from_input = st.session_state["week_from_input"]

st.subheader(f"Vecka: {week_from_input}")

list_week_days()

db = st.session_state["deta"].Base("workouts")
db_keys = [i["key"] for i in db.fetch()]

if st.session_state[f"Vecka {week_from_input} måndag"]:
    st.write("lägg till här")
    with st.expander("måndag"):
        st.selectbox("Välj pass"
                    , options = db_keys)
        

# Ange datum
    # Ange pass 1
        # Genomfört
        # Kommentar
    # Ange pass 2
        # Genomfört
        # Kommentar
# Ange datum
    # Ange pass 1
        # Gneomfört 
        # Kommentar