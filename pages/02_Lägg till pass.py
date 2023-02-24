import streamlit as st
from datetime import datetime
from deta import Deta

############################### Session state #################################
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

if "db" not in st.session_state:
    st.session_state["db"] =\
         st.session_state["deta"].Base("workouts")

################################# Functions ###################################

def update_workouts_db():
    dct_from_db = st.session_state["db"]\
        .get(st.session_state["workout name"])
    
    key_string = st.session_state["next_exercise"]
    dct_from_db.get("Övningar")\
        .update({key_string: st.session_state[key_string]})
    
    new_temp_dct = {"Övningar": dct_from_db["Övningar"]}
    st.session_state["db"].put(new_temp_dct
                    , key = st.session_state["workout name"])

def add_exercise():
    temp_dct = {"Övningar":{}}
    
    # if key already exist, insert throws an error
    try:
        st.session_state["db"].insert(temp_dct
        , key = st.session_state["workout name"])

        text_from_db = st.session_state["db"]\
        .get(st.session_state["workout name"])

        st.session_state["no_of_exercises"] =\
            len(text_from_db["Övningar"].keys())

        st.session_state["next_exercise"] =\
            f"Övning {st.session_state['no_of_exercises']+1}"
        
        st.text_input("Lägg till övning"
                    , on_change=update_workouts_db
                    , key=st.session_state["next_exercise"])  
    except:
        st.info("Namn upptaget")

        
   
    st.write(text_from_db)

def remove_workout():
    st.session_state["db"].delete(st.session_state["ta bort pass"])


def display_inlagda_pass():
    db = st.session_state["db"]

    lista_pass = [i["key"] for i in db.fetch().items]
    
    for item in lista_pass:
        st.write(item)

    st.selectbox("Ta bort ett pass"
                , options = ["Väl pass att ta bort"] + lista_pass
                , key = "ta bort pass"
                , on_change=remove_workout
                , label_visibility="collapsed")

################################## Program ####################################

st.header("Lägg till pass")
st.text_input("Ange namnet på passet du vill lägga till"
            , key = "workout name")

if st.session_state["workout name"]:
    add_exercise()

# st.checkbox("Visa alla inlagda pass"
#             , key = "Visa inlagda pass")

# if st.session_state["Visa inlagda pass"]:
#     display_inlagda_pass()
