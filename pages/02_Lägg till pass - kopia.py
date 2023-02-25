import streamlit as st
from datetime import datetime
from deta import Deta
from funcs import helper_funcs


############################### Session state #################################
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

################################# Variables ###################################
table = "workouts_new"
db = st.session_state["deta"].Base(table)

################################# Functions ###################################

def update_db(key, name, exercises, time, notes):
    dct = {"Namn":name
           , "Övningar": exercises
           , "Tidsåtgång (minuter)": time
           , "Anteckningar": notes
           }
    db.put(dct, key)

def workout_form():
    with st.form("my form", clear_on_submit=True):
        key = helper_funcs.generate_key(db)
        name = st.text_input("Ange namn på pass")
        exercises = st.text_area("Lägg in övningar")
        time = st.number_input("Uppskattad tidsåtgång (minuter)", value=30)
        notes = st.text_area("Allmänna anteckningar")
        submitted = st.form_submit_button("Skapa pass")
        if submitted:
            update_db(key
                      , name
                      , exercises
                      , time
                      , notes
                      )

def add_workout():
    workout_form()

def select_exercises():
    exercise_names = [item["Namn"] for item in db.fetch().items]
    options = st.multiselect("Välj pass att visa"
                             , exercise_names)
    return options

def display_workouts(options):
    workouts = db.fetch().items
    filtered_w = list(filter(lambda x: x['Namn'] in options, workouts))
    for w in filtered_w:
        with st.expander(w["Namn"]):
            st.write("**Övningar**")
            st.markdown(w["Övningar"])

            st.markdown(f"**Uppskattad tidsåtgång**")
            st.markdown(f"{w['Tidsåtgång (minuter)']} min")

            st.write("**Anteckningar**")
            st.markdown(w["Anteckningar"])


################################## Program ####################################

choice = helper_funcs.options_menu()

st.write(choice)

if choice == "add":
    add_workout()

if choice == "show":
    options = select_exercises()
    display_workouts(options)