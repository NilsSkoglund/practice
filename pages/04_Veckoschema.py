import streamlit as st
from datetime import datetime
from deta import Deta
# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

db_items = st.session_state["deta"].Base("Veckoscheman").fetch().items
db_items = sorted(db_items, key=lambda x: int(x["key"]))

def update_db(widget_str, week, day, workout):
    db = st.session_state["deta"].Base("Veckoscheman")
    db_item = db.get(week)
    db_item[day][workout][widget_str] =\
         st.session_state[f"{widget_str}{week}{day}{workout}"]



for item in db_items:
    st.header(f"Vecka {item['key']}")
    for day in st.session_state["lista_veckodagar"]:
        if len(item[day]) > 0:
            with st.expander(day):
                for key in item[day].keys():
                    st.write(item[day][key])
                    
                    st.subheader(key)

                    workout = st.session_state["deta"]\
                        .Base("workouts").get(key)["Övningar"]



                    for övning in workout:
                        övning_str = f"- {workout[övning]}"
                        st.markdown(övning_str)

                    
                    st.write("")

                    current_item = item[day][key]
                    genomfört = current_item["Genomfört"]
                    starttid = current_item["Starttid"]
                    sluttid = current_item["Sluttid"]
                    kommentar = current_item["Kommentar"]


                    genomfört_string = f"Genomfört{item['key']}{day}{key}"
                    
                    st.checkbox("Genomfört pass"
                                , value = genomfört
                                , key = genomfört_string
                                , on_change = update_db
                                , args=("Genomfört", item['key'], day, key))

                    
                    kommentar_string = f"Kommentar{item['key']}{day}{key}"
                    st.text_area("Kommentar"
                                , value = kommentar
                                , key = kommentar_string
                                , on_change = update_db
                                , args = ("Kommentar", item['key'], day, key))

                        

    

