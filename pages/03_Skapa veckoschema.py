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

st.subheader(f"Dagens datum: {datetime.now().date()}")
st.write(f"Veckonummer: {current_weak}")


# Skapa träningsvecka
st.date_input(
    "Välj veckostart för den vecka du vill skapa träningsschema för"
    , datetime.date(datetime.now())
    , key = "first_day_of_week"
)

if "first_day_of_week" in st.session_state:
    st.session_state["week_from_input"] =\
        str(st.session_state["first_day_of_week"].isocalendar().week)
    week_from_input = st.session_state["week_from_input"]
    db_name = "Veckoscheman"

    dct_temp = {"note":""}

    for day in st.session_state["lista_veckodagar"]:
        dct_temp[day] = {}

    try:
        st.session_state["deta"].Base(db_name)\
            .insert(dct_temp, key = f"{week_from_input}")
    except:
        pass
    


st.subheader(f"Vecka: {week_from_input}")

list_week_days()

db = st.session_state["deta"].Base("workouts")
st.session_state["workouts"] = [i["key"] for i in db.fetch().items]

def add_workout_to_weekly_schedule(day):
    db_name = "Veckoscheman"
    db = st.session_state["deta"].Base(db_name)
    
    week = st.session_state["week_from_input"]
    db_res = db.get(f"{week}")    

    pass_namn =  st.session_state[f"selectbox_{day}"]

    temp_dct = {"Starttid": {"timme":12, "minut": 0}
            , "Sluttid": {"timme":12, "minut": 0}
            , "Genomfört": False
            , "Kommentar": ""}

    db_res[day].update({pass_namn: temp_dct})

    db.put(db_res)

def remove_workout_from_schedule(week, day, workout):
    db = st.session_state["deta"].Base("Veckoscheman")
    item = db.get(week)
    del item[day][workout]
    db.put(item)



for day in st.session_state["lista_veckodagar"]:

    if st.session_state[day]:
        with st.expander(day):
            st.selectbox(""
                , options = st.session_state["workouts"]
                , key = f"selectbox_{day}"
                , on_change = add_workout_to_weekly_schedule
                , args = (day,)
                , label_visibility = "collapsed"
            )

            week_dct = st.session_state["deta"].Base("Veckoscheman")\
                .get(str(st.session_state["week_from_input"]))
            #st.markdown(f"**{day}**")
            if len(week_dct[day].keys()) == 0:
                st.markdown("- Inget pass inlagt")
            else:
                st.markdown("**Nedan visas inlagda pass. Klicka i boxen för att ta bort ett pass**")
                for workout in week_dct[day].keys():
                    week = st.session_state["week_from_input"]
                    key = f"Remove {week} {day} {workout}"
                    st.checkbox(workout
                                , key=key
                                , on_change=remove_workout_from_schedule
                                , args=(week, day, workout))