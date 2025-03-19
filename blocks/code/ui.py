import streamlit as st
from blocks.code.logic import Code_logic

class Code:
    def __init__(self):
        self.code_l = Code_logic()

    def start_page_display(self):
        st.session_state.start_page_s = False
        st.write("Startseite")
        st.button('Ich möchte einen Code kaufen', on_click=self.code_l.buy_code_status)
        st.button("Ich habe bereits einen Code und möchte das Assessment starten", on_click=self.code_l.enter_code_status)
        st.button("Admin", on_click=self.code_l.admin_start_page_status)
    
    def buy_code(self):
        st.session_state.buy_code_s = False
        st.write("Bestellfenster")
        st.write("Informationen zu Preiskategorien")
         
        placeholder = st.empty()
        with placeholder.form(key="buy_code_f", border=False):
            st.text_input("Vorname *", key="buy_code_f_vorname")
            st.text_input("Nachname *", key="buy_code_f_nachname")
            st.text_input("Email *", key="buy_code_f_email")
            st.text_input("Rechnungsadresse *", key="buy_code_f_rechnungsadresse")
            st.selectbox( "Zahlungsmittel *", ("EUR", "CHF", "USD"), key="buy_code_f_currency")
            st.number_input("Anzahl Codes", value=None, step = 1, key="buy_code_f_number_of_codes")
            st.form_submit_button('Kaufen', on_click=self.code_l.code_payment_status)

    def code_payment(self):
        st.session_state.code_payment_s = False
        self.code_l.generate_code()
        self.code_l.save_user()
        st.write("Zahlungsprozess")
        if st.session_state.buy_code_f_number_of_codes == 1:
            st.success('Der Code wurde generiert.')
        else:
            st.success('Die codes wurden generiert.')
        st.button("Startseite", on_click=self.code_l.home_page_status)

    def enter_code(self):
        st.session_state.enter_code_s = False
        st.write("Eingabe Code")
        placeholder = st.empty()
        with placeholder.form(key="enter_code_f", border=False):
            st.text_input("Eingabe Code", key ="enter_code_f_code")
            st.form_submit_button('Weiter', on_click=self.code_l.check_code)
        st.button("Startseite", on_click=self.code_l.home_page_status)

    def enter_code_password(self):
        st.session_state.enter_code_s = False
        st.write("Eingabe Code")
        placeholder = st.empty()
        with placeholder.form(key="enter_code_pass_f", border=False):
            st.text_input("Eingabe Code", f"{st.session_state.entered_code}", key ="enter_code_pass_f_code")
            st.text_input("Passwort", key ="enter_code_pass_f_password")
            st.form_submit_button('Weiter', on_click=self.code_l.check_code_pass)
        st.button("Startseite", on_click=self.code_l.home_page_status)

    def code_information(self):
        st.session_state.check_code_result_s = False
        session_status = "start"
        self.code_l.save_session(st.session_state.entered_code, session_status)
        st.write("Informationsseite")
        st.write("“Informed consent” und “Informationen zum Assessment” ")
        st.button("Start questionnaire", on_click=self.code_l.questionnaire_status)
        