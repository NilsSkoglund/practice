import streamlit as st
from datetime import datetime
from deta import Deta

def vallen_skivstång():
    st.markdown("""
    **Vallen Skivstång 60 min + bastu 17:30-19:30**
    - Benböj 5x5 (90kg)
    - Marklyft 5x5 (120kg)
    - Frivändningar 5x5 (67.5kg)
    - Bänkpress 5x5 (75kg)
    """)    

def stretch():
    st.markdown("""
    **Valfri stretch 15 min 07:15-07:30**
    - Morgonrutin från den där duden
    - Yin-yoga övning där man lutar sig bakåt
    """)

def meditation():
    st.markdown("""
    **Meditation 15 min 07:45-08:15**
    - Klä dig varmt
    - Gå till berget och meditera i 15 min
    - Ta med mobil för att ta tid
    """)

def sats_cardio():
    st.markdown(
    """
    **Gym Cardio 40/20 x2 06:45-07:15**
    - KB Swings (32kg)
    - PU Deadlift (18 kg x2 Kettle Bell)
    - Slam balls (12kg)
    - Hoppa på box
    - KB Snatch (18 kg x2 Kettle Bell)
    - Boll över axel (30kg)
    - Barbell Thrusters (30kg)
    - Cleans (30kg)
    - Planka
    - Burpees 
    """)

def chins():
    st.markdown(
    """
    **Chins x20 under 10-15 minuter valfri tid**
    - 4 - 3 - 3
    - 4 - 3 - 3
    """)

def armhävningar():
    st.markdown(
    """
    **Armhävningar x200 under valfri tid**
    - 20 x 10
    """)

def get_week():
    return datetime.isocalendar(datetime.now()).week

st.header(f"Schema Vecka 7, 8 & 9")
st.markdown("*Sista träningsdag: 3e mars*")

with st.expander("Måndag"):
    sats_cardio()
    st.write("")

    meditation()
    st.write("")

    vallen_skivstång()
    st.write("")

with st.expander("Tisdag"):
    stretch()
    st.write("")

    meditation()
    st.write("")

    chins()
    st.write("")

with st.expander("Onsdag"):
    sats_cardio()
    st.write("")

    meditation()
    st.write("")

    armhävningar()
    st.write("")

with st.expander("Torsdag"):
    stretch()
    st.write("")
    
    meditation()
    st.write("")

    chins()
    st.write("")

with st.expander("Fredag"):
    sats_cardio()
    st.write("")

    meditation()
    st.write("")

    vallen_skivstång()
    st.write("")

