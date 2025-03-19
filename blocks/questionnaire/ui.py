import streamlit as st
from blocks.questionnaire.logic import Questionnaire_logic

class Questionnaire:
    def __init__(self):
        self.questionnaire_l = Questionnaire_logic()

    def show_question(self):

        st.session_state.questionnaire_s = False
        
        st.session_state.question_number += 1
        session_status = "question"+str(st.session_state.question_number)
        self.questionnaire_l.save_session(st.session_state.entered_code, session_status)
        st.write(f"Frage #: {st.session_state.question_number}")
        question_text, subquestions = self.questionnaire_l.get_question_content()
        st.write(question_text)

        radio_butt_opt = ["o1","o2","o3","o4","o5","o6","o7"]

        placeholder = st.empty()
        with placeholder.form(key="question_f",border=False):

            cols = st.columns(spec=[0.2, 0.1, 0.6, 0.1])
            cols[1].markdown("Strongly disagree") # !!!
            cols[3].markdown("Strongly agree") # !!!

            for subq in subquestions:
                cols = st.columns(spec=[0.2, 0.8])
                with cols[0]:
                    cols[0].write(subq)
                with cols[1]:
                    if subq==subquestions[0]:
                        st.radio("label1",radio_butt_opt,key=f"rb_answer1", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[1]:
                        st.radio("label2",radio_butt_opt,key=f"rb_answer2", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[2]:
                        st.radio("label3",radio_butt_opt,key=f"rb_answer3", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[3]:
                        st.radio("label4",radio_butt_opt,key=f"rb_answer4", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[4]:
                        st.radio("label5",radio_butt_opt,key=f"rb_answer5", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[5]:
                        st.radio("label6",radio_butt_opt,key=f"rb_answer6", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[6]:
                        st.radio("label7",radio_butt_opt,key=f"rb_answer7", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[7]:
                        st.radio("label8",radio_butt_opt,key=f"rb_answer8", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[8]:
                        st.radio("label9",radio_butt_opt,key=f"rb_answer9", horizontal=True, index=None, label_visibility="collapsed")
                    elif subq==subquestions[9]:
                        st.radio("label10",radio_butt_opt,key=f"rb_answer10", horizontal=True, index=None, label_visibility="collapsed")
            st.form_submit_button('Weiter', on_click=self.questionnaire_l.questionnaire_status)


