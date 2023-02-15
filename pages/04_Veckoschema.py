import streamlit as st
from datetime import datetime
from deta import Deta
# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

db_items = st.session_state["deta"].Base("Veckoscheman").fetch().items
db_items = sorted(db_items, key=lambda x: int(x["key"]))

for item in db_items:
    st.header(f"Vecka {item['key']}")
    for day in st.session_state["lista_veckodagar"]:
        if len(item[day]) > 0:
            with st.expander(day):
                for key in item[day].keys():
                    st.write(key)

                    workout = st.session_state["deta"]\
                        .Base("workouts").get(key)["Övningar"]


                    for övning in workout:
                        övning_str = f"- {workout[övning]}"
                        st.markdown(övning_str)

                        

    

