import streamlit as st
from datetime import datetime, time
from deta import Deta
# functions
def add_comment(quarter):
    db = Deta(st.secrets["deta_key"]).Base("Quarterly goals")
    item = db.get(quarter)
    next_comment_no = len(item["Comments"]) + 1
    item["Comments"].update(f"Comment{next_comment_no}:{st.session_state[f'add_comment{quarter}']}")


# Connect to Deta Base with your Project Key
if "deta" not in st.session_state:
    st.session_state["deta"] = Deta(st.secrets["deta_key"])


db = Deta(st.secrets["deta_key"]).Base("Quarterly goals")
## Q1
quarter = "Q1"
temp_dct = {"Comments":{}, "Goals":{}}
try:
    db.insert(temp_dct, key=quarter)
except:
    pass
## Lägg till Kommentar
    ## Text  area
key_add_comment = "Lägg till kommentar"
st.checkbox(key_add_comment
            , key = f"{quarter}{key_add_comment}")

if st.session_state[f"{quarter}{key_add_comment}"]:
    st.text_area(""
                , key=f"add_comment{quarter}"
                , on_change=add_comment
                , args=quarter)

item = db.get(quarter)

for comment in item["Comments"].keys():
    st.text_are(""
                , value = item["Comments"][comment])

## Lägg till mål
    ## Lägg till namn på mål
    ## Lägg till checkbox