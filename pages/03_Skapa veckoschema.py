import streamlit as st
from datetime import datetime
from deta import Deta

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

################################# Functions ###################################
def list_week_days():    
    col1, col2 = st.columns(2)

    stop_index = 4
    with col1:
        for day in st.session_state["lista_veckodagar"][:stop_index]:
            st.checkbox(
                f"Lägg till pass {day}"
                , key = day
            )
    with col2:
        for day in st.session_state["lista_veckodagar"][stop_index:]:
            st.checkbox(
                f"Lägg till pass {day}"
                , key = day
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

def add_workout_to_weekly_schedule(day):
    week = st.session_state["week_from_input"]
    st.write(f"{week}{day}")

for day in st.session_state["lista_veckodagar"]:

    if st.session_state[day]:
        st.write("lägg till här")
        with st.expander(day):
            st.selectbox("Välj pass"
                        , options = st.session_state["workouts"]
                        , key = f"selectbox_{day}"
                        , on_change = add_workout_to_weekly_schedule
                        , args = (day,)
            )



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