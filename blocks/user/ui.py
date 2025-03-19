import streamlit as st
from blocks.user.logic import User_logic

class User:
    def __init__(self):
        self.user_l = User_logic()

    def demographic_vars_input(self):
        st.session_state.demographic_vars_s = False
        st.write("Demographische Variable")
        placeholder = st.empty()
        with placeholder.form(key="demographic_vars_f", border=False):
            st.text_input("Passwort", key="demographic_vars_f_password")
            st.text_input("Vorname", key="demographic_vars_f_vorname")
            st.text_input("Name", key="demographic_vars_f_name")
            st.number_input("Alter", value=None, step = 1, key="demographic_vars_f_age")
            st.radio("Geschlecht",["f","m","d"],key=f"demographic_vars_f_gender", horizontal=True, index=None, label_visibility="collapsed")
            st.selectbox( "Berufserfahrung", tuple(range(0,10)), key="demographic_vars_f_workexp")
            st.form_submit_button('Weiter', on_click=self.user_l.finish_questionnaire_status)


