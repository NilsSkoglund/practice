import streamlit as st
import string
import random

def options_menu():
    vy = st.radio("Välj vy"
            , ("Visningsvy", "Redigeringsvy")
            , horizontal=True
            , label_visibility="collapsed")
            
    st.markdown("---")

    if vy == "Redigeringsvy":

        val_redigering = st.radio("Välj ..."
                                , ("Lägg till", "Redigera", "Ta bort")
                                , horizontal=True
                                , label_visibility="collapsed")

        if val_redigering == "Lägg till":
            st.write("---")
            return "add"
        elif val_redigering == "Redigera":
            st.write("---")
            return "edit"
        elif val_redigering == "Ta bort":
            st.write("---")  
            return "remove"

    elif vy == "Visningsvy":
        return "show"
    
def generate_key(db):
    ''' 
    Requires a deta base "table" as argument
    Generate a random key used in db and in session state
    Makes sure that key doesn't already exist in passed db 
    '''
    ascii = string.ascii_uppercase
    key = "".join([random.choice(ascii) for i in range(16)])

    items = db.fetch().items
    keys = [i["key"] for i in items]
    while key in keys:
        key = "".join([random.choice(ascii) for i in range(16)])