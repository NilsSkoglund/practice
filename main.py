import streamlit as st
from datetime import datetime
from deta import Deta
# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

if "exercise_counter" not in st.session_state:
    st.session_state["exercise_counter"] = 1

def add_exercise_func():
    st.write("HAJ FROM FUNC")
    key_string = f"Övning {st.session_state['exercise_counter']}"
    new_temp_dct = {key_string: st.session_state[key_string]}
    st.write(key_string)
    st.write(temp_dct)

    st.session_state["db"].put({"Övningar": new_temp_dct}
                                , key = st.session_state["workout name"])
    st.session_state["exercise_counter"]+=1
    st.write(st.session_state["exercise_counter"])


st.text_input("Ange namnet på passet"
            , key = "workout name")
if st.session_state["workout name"]:
    st.session_state["db"] = st.session_state["deta"].Base("workouts")
    st.write("Haj")
    # connect to database
    # database name based on username - new session state variable
    temp_dct = {"Övningar":{}}
    try:
        st.session_state["db"].insert(temp_dct
        , key = st.session_state["workout name"])
    except:
        pass

    st.text_input("Lägg till övning"
                                , on_change=add_exercise_func
                                , key=f"Övning {st.session_state['exercise_counter']}")       
        
    
    text_from_db = st.session_state["db"].get(st.session_state["workout name"])

    st.write(text_from_db)
    st.write(st.session_state["exercise_counter"])





# def register_new_session_in_db():
#     # Create row in db including session key
#     st.session_state["db"].put(temp_dct\
#                                 , key=st.session_state["db_session_key"])

# def get_all_items_from_db(db):
#     # Get items from db (limit is 1000 so while loop is added for robustness)
#     res = db.fetch()
#     all_items = res.items
#     # fetch until last is 'None'
#     while res.last:
#         res = db.fetch(last=res.last)
#         all_items += res.items
#     return all_items

# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

# connect to database
# database name based on username - new session state variable
st.session_state["db"] =\
st.session_state["deta"].Base("NILLE")


def update_db():
    st.session_state["db"].put({
    "genomfört": st.session_state["test"],
    "key": "test"
})

st.session_state["test"] = st.session_state["db"].get("test").get("genomfört")

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
    st.checkbox("Genomfört"
    , key="test"
    , on_change=update_db)

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

