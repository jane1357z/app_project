import streamlit as st
from datetime import date,datetime
from blocks.user.data import User_data

class User_logic:
    def __init__(self):
        self.user_d = User_data()
    def user_profile_status(self):
        st.session_state.user_profile_s = True
    def finish_questionnaire_status(self):
        if st.session_state.demographic_vars_f_password == None:
            st.warning('Bitte, füllen Sie Passwort aus.')
            st.session_state.demographic_vars_s = True
        else:
            self.add_user()
            st.session_state.finish_questionnaire_s = True

    def add_user(self):
        today = datetime.strptime(date.today().strftime('%d.%m.%Y'), "%d.%m.%Y") 
        row_data = (st.session_state.entered_code, today, st.session_state.demographic_vars_f_password,st.session_state.demographic_vars_f_name,st.session_state.demographic_vars_f_vorname, st.session_state.demographic_vars_f_age, st.session_state.demographic_vars_f_gender, st.session_state.demographic_vars_f_workexp)
        columns = 'Code, Datum, [Indiv. PW], Name, Vorname, [Alter], Geschlecht, Berufserfahrung'
        table_name = "Users"
        self.user_d.insert_row(columns, row_data, table_name)