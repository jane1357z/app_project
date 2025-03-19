import streamlit as st
from blocks.questionnaire.data import Questionnaire_data


class Questionnaire_logic:
    def __init__(self):
        self.questionnaire_d = Questionnaire_data()

    def home_page_status(self):
        st.session_state.start_page_s = True
    def questionnaire_status(self):
        rb_answers = []
        rb_answers.append(st.session_state.rb_answer1)
        rb_answers.append(st.session_state.rb_answer2)
        rb_answers.append(st.session_state.rb_answer3)
        rb_answers.append(st.session_state.rb_answer4)
        rb_answers.append(st.session_state.rb_answer5)
        rb_answers.append(st.session_state.rb_answer6)
        rb_answers.append(st.session_state.rb_answer7)
        rb_answers.append(st.session_state.rb_answer8)
        rb_answers.append(st.session_state.rb_answer9)
        rb_answers.append(st.session_state.rb_answer10)
        if None in rb_answers:
            st.warning('Beantworten Sie alle Fragen')
            st.session_state.question_number -=1
            st.session_state.questionnaire_s = True
        else:
            st.session_state.rb_answer1 = None
            st.session_state.rb_answer2 = None
            st.session_state.rb_answer3 = None
            st.session_state.rb_answer4 = None
            st.session_state.rb_answer5 = None
            st.session_state.rb_answer6 = None
            st.session_state.rb_answer7 = None
            st.session_state.rb_answer8 = None
            st.session_state.rb_answer9 = None
            st.session_state.rb_answer10 = None

            self.questionnaire_d.add_answers(st.session_state.entered_code, st.session_state.question_number, rb_answers)
            if st.session_state.question_number <2:#< st.session_state.total_question_number:
                st.session_state.questionnaire_s = True
            elif st.session_state.question_number ==2:#== st.session_state.total_question_number:
                session_status = "demogr"
                self.save_session(st.session_state.entered_code, session_status)
                st.session_state.demographic_vars_s = True

    def finish_questionnaire_status(self):
        st.session_state.finish_questionnaire_s = True

    def get_question_content(self):
        question_counter = st.session_state.question_number-1
        questions = self.questionnaire_d.get_question("Example_options")[question_counter]
        sub_options = self.questionnaire_d.get_suboptions("Example_options")[question_counter]
        return questions, sub_options
    
    def save_session(self, code, status):
        self.questionnaire_d.update_session(code, status)