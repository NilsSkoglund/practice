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
   st.subheader("Skapa mål")
   kvartal = st.radio(
        "För vilket kvartal gäller målet?"
        , ('Q1', 'Q2', 'Q3', 'Q4')
        , horizontal=True)
   namn = st.text_input("Namn på målet")
   beskrivning = st.text_input("Beskriv ditt mål")
   datum = st.date_input("När ska målet vara uppnåt?")
   noteringar = st.text_area("Övriga anteckningar")

   submitted = st.form_submit_button("Skapa mål")

   if submitted:
    key = kvartal+namn
    temp_dct = {"namn":namn
                , "kvartal":kvartal
                , "beskrivning":beskrivning
                , "datum": datum
                , "noteringar":noteringar}
    st.write(temp_dct)
    st.experimental_rerun()