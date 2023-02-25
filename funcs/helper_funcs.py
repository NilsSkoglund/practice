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
        skapa_mål_func(välj_kvartal, välj_år)
    elif val_redigering == "Redigera":
        st.write("---")
        edit_goals(välj_kvartal, välj_år)
    elif val_redigering == "Ta bort":
        st.write("---")
        meny_ta_bort_mål(välj_kvartal, välj_år)    

elif vy == "Visningsvy":
    display_goals(välj_kvartal, välj_år)