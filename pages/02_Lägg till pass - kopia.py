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
def workout_name():
    name = st.text_input("Ange namn på pass")
    workout_added = False
    try:
        db.insert(name)
        workout_added = True
    except:
        st.info("Namn finns redan. Välj ett annat namn.")
    return workout_added, name

def update_db(name, exercises):
    dct = {"Övningar": exercises}
    db.update(dct, name)

def workout_form(name):
    with st.form(name):
        exercises = st.text_area("Lägg in övningar")
        submitted = st.form_submit_button("Skapa pass")
        if submitted:
            update_db(name, exercises)

def add_workout():
    workout_added, name = workout_name()
    if workout_added:
        workout_form(name)

################################## Program ####################################

choice = helper_funcs.options_menu()

st.write(choice)

if choice == "add":
    add_workout()