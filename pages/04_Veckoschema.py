import streamlit as st
from datetime import datetime, time
from deta import Deta
# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])

db_items = st.session_state["deta"].Base("Veckoscheman").fetch().items
db_items = sorted(db_items, key=lambda x: int(x["key"]))

def exercise_widgets_update_db(widget_str, week, day, workout):
    db = st.session_state["deta"].Base("Veckoscheman")
    db_item = db.get(week)
    if widget_str in ["Genomfört", "Kommentar"]:
        db_item[day][workout][widget_str] =\
            st.session_state[f"{widget_str}{week}{day}{workout}"]
    else:
        time_object = st.session_state[f"{widget_str}{week}{day}{workout}"]
        db_item[day][workout][widget_str]["timme"] = time_object.hour
        db_item[day][workout][widget_str]["minut"] = time_object.minute

weeks = [i["key"] for i in db_items]

for week in weeks:
    key = f"Visa vecka {week}"
    st.checkbox(f"Vecka {week}"
                , key = key)

display_weeks = []

for week in weeks:
    if st.session_state[f"Visa vecka {week}"]:
        display_weeks.append(week)

for item in db_items:
    if item["key"] in display_weeks:
        st.header(f"Vecka {item['key']}")
        for day in st.session_state["lista_veckodagar"]:
            if len(item[day]) > 0:
                with st.expander(day):
                    for key in item[day].keys():
                        
                        st.markdown("---")
                        st.subheader(key)

                        workout = st.session_state["deta"].Base("workouts")\
                            .get(key)["Övningar"]

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
                                    , on_change = exercise_widgets_update_db
                                    , args=("Genomfört", item['key'], day, key))
                        
                        kommentar_string = f"Kommentar{item['key']}{day}{key}"
                        st.text_area("Kommentar"
                                    , value = kommentar
                                    , key = kommentar_string
                                    , on_change = exercise_widgets_update_db
                                    , args = ("Kommentar", item['key'], day, key))
                        
                        starttid_string = f"Starttid{item['key']}{day}{key}"
                        st.time_input("Starttid"
                                    , value = time(starttid["timme"], starttid["minut"])
                                    , key = starttid_string
                                    , on_change = exercise_widgets_update_db
                                    , args = ("Starttid", item['key'], day, key))
                        
                        sluttid_string = f"Sluttid{item['key']}{day}{key}"
                        st.time_input("Sluttid"
                                    , value = time(sluttid["timme"], sluttid["minut"])
                                    , key = sluttid_string
                                    , on_change = exercise_widgets_update_db
                                    , args = ("Sluttid", item['key'], day, key))

                    

                        

    

