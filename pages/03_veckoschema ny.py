import streamlit as st
from datetime import datetime
from deta import Deta
from funcs import helper_funcs

############################### Session state #################################
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

################################# Variables ###################################
table = "weekly_schedule"
db = st.session_state["deta"].Base(table)

current_weak = datetime.now().date().isocalendar().week

lista_veckodagar = [
    "måndag"
    , "tisdag"
    , "onsdag"
    , "torsdag"
    , "fredag"
    , "lördag"
    , "söndag"
]
db_workouts = st.session_state["deta"].Base("workouts_new")
workouts = [i["Namn"] for i in db_workouts.fetch().items]

################################# Functions ###################################
def options_menu():
    '''
    Options menu for weekly schedule.
    Differs from other options menu...
    ... since add and edit are bundled together
    '''
    vy = st.radio("Välj vy"
            , ("Visningsvy", "Redigeringsvy")
            , horizontal=True
            , label_visibility="collapsed")
            
    st.markdown("---")

    if vy == "Redigeringsvy":

        val_redigering = st.radio("Välj ..."
                                , ("Lägg till/Redigera",  "Ta bort")
                                , horizontal=True
                                , label_visibility="collapsed")

        if val_redigering == "Lägg till/Redigera":
            st.write("---")
            return "add/edit"
        
        elif val_redigering == "Ta bort":
            st.write("---")  
            return "remove"

    elif vy == "Visningsvy":
        return "show"

def choose_week():
    st.date_input(
    "Välj veckostart för den vecka du vill skapa/redigera träningsschema för"
    , datetime.date(datetime.now())
    , key = "first_day_of_week"
    )

    if "first_day_of_week" in st.session_state:
        week_from_input =\
            str(st.session_state["first_day_of_week"].isocalendar().week)
    
    return week_from_input

def insert_weekly_schedule_db(chosen_week):
    '''
        Create a new entry for chosen week in db
        Insert will throw an error if week already exists in db
    '''
    dct_temp = {"note":""}
    for day in lista_veckodagar:
        dct_temp[day] = {}
    try:
        db.insert(dct_temp, key = f"{chosen_week}")
    except:
        pass

def list_days():    
    col1, col2 = st.columns(2)

    stop_index = 4
    with col1:
        for day in lista_veckodagar[:stop_index]:
            st.checkbox(
                f"Lägg till pass {day}"
                , key=day
            )
    with col2:
        for day in lista_veckodagar[stop_index:]:
            st.checkbox(
                f"Lägg till pass {day}"
                , key=day
            )

def add_workout_to_weekly_schedule(day, week):
    if st.session_state[f"selectbox_{day}"] != "Välj pass":
        db_res = db.get(f"{week}")    
        pass_namn =  st.session_state[f"selectbox_{day}"]
        temp_dct = {"Genomfört": False
                , "Kommentar": ""}
        db_res[day].update({pass_namn: temp_dct})
        db.put(db_res)
    else:
        pass

def remove_workout_from_schedule(week, day, workout):
    item = db.get(week)
    del item[day][workout]
    db.put(item)

def loop_days(chosen_week):
    for day in lista_veckodagar:

        if st.session_state[day]:
            with st.expander(day):
                st.selectbox(""
                    , options = ["Välj pass"] + workouts
                    , key = f"selectbox_{day}"
                    , on_change = add_workout_to_weekly_schedule
                    , args = (day, chosen_week, )
                    , label_visibility = "collapsed"
                )

                week_dct = db.get(chosen_week)
                #st.markdown(f"**{day}**")
                if len(week_dct[day].keys()) == 0:
                    st.markdown("- Inget pass inlagt")
                else:
                    st.markdown("**Nedan visas inlagda pass.\
                                 Klicka i boxen för att ta bort ett pass**")
                    for workout in week_dct[day].keys():
                        week = st.session_state["week_from_input"]
                        key = f"Remove {week} {day} {workout}"
                        st.checkbox(workout
                                    , key=key
                                    , on_change=remove_workout_from_schedule
                                    , args=(week, day, workout))


def add_weekly_schedule():
    chosen_week = choose_week()
    insert_weekly_schedule_db(chosen_week)
    st.subheader(f"Vecka: {chosen_week}")
    list_days()
    loop_days(chosen_week)

################################## Program ####################################
st.subheader(f"Dagens datum: {datetime.now().date()}")
st.write(f"Veckonummer: {current_weak}")

choice = options_menu()

if choice == "show":
    st.write("show")

if choice == "add/edit":
    st.write("add/edit")
    add_weekly_schedule()

if choice == "remove":
    st.write("remove")
