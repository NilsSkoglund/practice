import streamlit as st
from datetime import datetime
from deta import Deta
# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

if "db" not in st.session_state:
    st.session_state["db"] =\
         st.session_state["deta"].Base("workouts")


def add_exercise_func():
    dct_from_db = st.session_state["db"]\
        .get(st.session_state["workout name"])
    
    key_string = st.session_state["next_exercise"]
    dct_from_db.get("Övningar")\
        .update({key_string: st.session_state[key_string]})
    
    new_temp_dct = {"Övningar": dct_from_db["Övningar"]}
    st.session_state["db"].put(new_temp_dct
                    , key = st.session_state["workout name"])

st.header("Lägg till pass")
st.text_input("Ange namnet på passet du vill lägga till"
            , key = "workout name")

if st.session_state["workout name"]:
    
    temp_dct = {"Övningar":{}}
    
    # if key already exist, insert throws an error
    try:
        st.session_state["db"].insert(temp_dct
        , key = st.session_state["workout name"])
    except:
        pass

    text_from_db = st.session_state["db"]\
        .get(st.session_state["workout name"])

    st.session_state["no_of_exercises"] =\
         len(text_from_db["Övningar"].keys())

    st.session_state["next_exercise"] =\
         f"Övning {st.session_state['no_of_exercises']+1}"
    
    st.text_input("Lägg till övning"
                , on_change=add_exercise_func
                , key=st.session_state["next_exercise"])       
   

    st.write(text_from_db)

st.checkbox("Visa alla inlagda pass"
            , key = "Visa inlagda pass")

def remove_workout():
    st.session_state["db"].delete(st.session_state["ta bort pass"])

if st.session_state["Visa inlagda pass"]:
    db = st.session_state["db"]

    lista_pass = [i["key"] for i in db.fetch().items]
    
    for item in lista_pass:
        st.write(item)

    st.selectbox("Ta bort ett pass"
                , options = lista_pass
                , key = "ta bort pass"
                , on_change=remove_workout)
    
