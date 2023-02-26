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

    
def options_menu_dev(page):
    key = "vy"
    vy = st.radio("Välj vy"
            , ("Visningsvy", "Redigeringsvy")
            , horizontal=True
            , label_visibility="collapsed"
            , key=st.session_state[key+page])
            
    st.markdown("---")

    if st.session_state[key+page] == "Visningsvy":
        return "show"

    if st.session_state[key+page] == "Redigeringsvy":
        key = "val_redigering"
        val_redigering = st.radio("Välj ..."
                                , ("Lägg till", "Redigera", "Ta bort")
                                , horizontal=True
                                , label_visibility="collapsed"
                                , key=st.session_state[key+page])

        if st.session_state[key+page] == "Lägg till":
            st.write("---")
            return "add"
        elif st.session_state[key+page] == "Redigera":
            st.write("---")
            return "edit"
        elif st.session_state[key+page] == "Ta bort":
            st.write("---")  
            return "remove"

    
    
def generate_key(db):
    ''' 
    Requires a deta base "table" as argument
    Generate a random key used in db and in session state
    Makes sure that the key doesn't already exist in table 
    '''
    def randomize_key():
        ascii = string.ascii_uppercase
        return "".join([random.choice(ascii) for i in range(16)])
    
    key = randomize_key()
    items = db.fetch().items
    keys = [i["key"] for i in items]
    while key in keys:
        key = randomize_key()