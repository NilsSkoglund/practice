import streamlit as st
from datetime import datetime
from deta import Deta

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

################################# Functions ###################################
def list_week_days():    
    for i in st.session_state["lista_veckodagar"]:
        st.checkbox(
            f"Lägg till pass {i}"
            , key = i
        )

################################# Program #####################################

st.session_state["lista_veckodagar"] = [
    "måndag"
    , "tisdag"
    , "onsdag"
    , "torsdag"
    , "fredag"
    , "lördag"
    , "söndag"
]

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
if week_from_input: 
    db_name = "Veckoscheman"
    db = st.session_state["deta"].Base(db_name)
    dct_temp = {"Vecka": 0
            , "Måndag": ""
            , "Tisdag": ""
            , "Onsdag": ""
            , "Torsdag": ""
            , "Fredag": ""
            , "Lördag": ""
            , "Söndag": ""}

    dct_temp["Vecka"] = week_from_input
    


st.subheader(f"Vecka: {week_from_input}")

list_week_days()

db = st.session_state["deta"].Base("workouts")
st.session_state["workouts"] = [i["key"] for i in db.fetch().items]

for day in st.session_state["lista veckodagar"]:

    if st.session_state[day]:
        st.write("lägg till här")
        with st.expander(day):
            st.selectbox("Välj pass"
                        , options = st.session_state["workouts"]
            )


# if st.session_state[f"Vecka {week_from_input} måndag"]:
#     st.write("lägg till här")
#     with st.expander("måndag"):
#         st.selectbox("Välj pass"
#                     , options = st.session_state["workouts"]
#                     , on_change = add_workout)
        

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