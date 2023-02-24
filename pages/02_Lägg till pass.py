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
    st.session_state["db"].put(temp_dct
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

    st.write(text_from_db)


def add_workout():

    add_exercise()

    

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

def check_if_key_exits():
    if st.session_state["db"].get(st.session_state["workout name"]):
        return True
    else:
        return False

def already_checked():
    return st.session_state["checked workout name"] ==\
         st.session_state["workout name"]

################################## Program ####################################

st.header("Lägg till pass")
st.text_input("Ange namnet på passet du vill lägga till"
            , key = "workout name")

st.session_state["checked workout name"] = ""


if st.session_state["workout name"]:
    if check_if_key_exits() and not already_checked():
        st.info("Name already exists")
    else:
        st.session_state["checked workout name"] =\
            st.session_state["workout name"]
    
    
        add_workout()


# st.checkbox("Visa alla inlagda pass"
#             , key = "Visa inlagda pass")

# if st.session_state["Visa inlagda pass"]:
#     display_inlagda_pass()
