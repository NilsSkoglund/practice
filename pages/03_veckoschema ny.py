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

################################# Functions ###################################


################################## Program ####################################

choice = helper_funcs.options_menu()

if choice == "show":
    st.write("show")

if choice == "add":
    st.write("add")

if choice == "edit":
    st.write("edit")

if choice == "remove":
    st.write("remove")
