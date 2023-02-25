import streamlit as st
from datetime import datetime
from deta import Deta
from funcs import helper_funcs

choice = helper_funcs.options_menu()

st.write(choice)

############################### Session state #################################
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

################################# Variables ###################################
table = "workouts_new"
db = st.session_state["deta"].Base(table)

################################# Functions ###################################
