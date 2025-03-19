import streamlit as st
from blocks.code.data import Code_data
import uuid
from datetime import date,datetime


class Code_logic:
    def __init__(self):
        self.code_d = Code_data()

    def home_page_status(self):
        st.session_state.enter_code_password_s = False
        st.session_state.start_page_s = True
    
    def enter_code_status(self):
        st.session_state.enter_code_s = True
        
    def buy_code_status(self):
        st.session_state.buy_code_s = True

    def code_payment_status(self):
        form_list = [st.session_state.buy_code_f_vorname, st.session_state.buy_code_f_nachname, st.session_state.buy_code_f_email,
                     st.session_state.buy_code_f_rechnungsadresse, st.session_state.buy_code_f_currency, st.session_state.buy_code_f_number_of_codes]
        if None in form_list or '' in form_list:
            form_list.clear()
            st.session_state.buy_code_s = True
            st.warning('Bitte, füllen Sie die Pflicht-Textfelder aus.')
        else:
            st.session_state.code_payment_s = True

    def check_code(self):
        st.session_state.entered_code = st.session_state.enter_code_f_code
        row = self.code_d.get_row("Codes", st.session_state.entered_code, "Code")

        if row != False:
            if row[2] == "generiert": # generated and active, but not activated
                self.code_d.update_code_status(st.session_state.entered_code, "aktiviert", "Codes")
                st.session_state.check_code_result_s = True
            elif row[2] == "abgelaufen": # expired
                st.info("Der Code ist abgelaufen.")
                st.session_state.enter_code_s = True
            elif row[2] == "aktiviert": # activated, go to session
                session_row = self.code_d.get_row("Example_Session", st.session_state.entered_code, "Code")
                if session_row[1] == "start":
                    st.session_state.check_code_result_s = True
                elif "question" in session_row[1]:
                    st.session_state.question_number = int(session_row[1][-1])-1
                    st.session_state.total_question_number = self.code_d.get_number_of_questions("Example_options")
                    st.session_state.questionnaire_s = True
                elif session_row[1] == "demogr":
                    st.session_state.demographic_vars_s = True
                elif session_row[1] == "feedback":
                    st.session_state.enter_code_password_s = True
        else: # not generated
            st.error("Der Code ist inkorrekt.")
            st.session_state.enter_code_s = True

    def check_code_pass(self):
        entered_password = st.session_state.enter_code_pass_f_password
        row = self.code_d.get_row("Users", st.session_state.entered_code, "Code")
        if entered_password == row[2]:
            st.session_state.enter_code_password_s = False
            st.session_state.finish_questionnaire_s = True
        else:
            st.error("Das Passwort ist inkorrekt.")

    def questionnaire_status(self):
        st.session_state.total_question_number = self.code_d.get_number_of_questions("Example_options")
        st.session_state.questionnaire_s = True
        
    def admin_start_page_status(self):
        st.session_state.admin_start_page_s = True

    def generate_code(self):
        for _ in range(st.session_state.buy_code_f_number_of_codes):
            generated_codes = self.code_d.get_col_list("Codes", "Code")
            code = str(uuid.uuid4().hex)[:10]
            while (code in generated_codes):
                code = str(uuid.uuid4().hex)[:10]
            # today = date.today().strftime('%d.%m.%Y')
            today = datetime.strptime(date.today().strftime('%d.%m.%Y'), "%d.%m.%Y") 
            status = "generiert"
            self.code_d.insert_code(code, today, status)

    def save_user(self):
        # save to users table
        pass

    def save_session(self, code, status):
        self.code_d.insert_session(code, status)

        