import streamlit as st

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
        elif val_redigering == "Redigera":
            st.write("---")
        elif val_redigering == "Ta bort":
            st.write("---")   

    elif vy == "Visningsvy":
        st.write("visningsvy")