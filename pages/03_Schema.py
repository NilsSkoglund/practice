import streamlit as st
from datetime import datetime
from deta import Deta

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])


# Skapa träningsvecka
st.date_input(
    "Veckostart"
    , datetime.date(datetime.now())
    , key = "first_day_of_week"
)

st.session_state["current_week"] =\
     datetime.now().date().isocalendar().week

st.session_state["week_from_input"] =\
     st.session_state["first_day_of_week"].isocalendar().week

st.write(st.session_state["current_week"])
st.write(st.session_state["week_from_input"])

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