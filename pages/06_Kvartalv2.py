import streamlit as st
from datetime import datetime, time
from deta import Deta

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

db = st.session_state["deta"].Base("Quarterly_goals")

# Add goal - Button?

# Open form
    # name - text input
    # specify goal - text input
with st.form("my_form"):
   st.write("Inside the form")
   name = st.text_input("Namn på målet")
   beskrivning = st.text_input("Beskriv ditt mål")
   