import streamlit as st
from blocks.feedback.logic import Feedback_logic

class Feedback:
    def __init__(self):
        self.feedback_l = Feedback_logic()

    def show_end_quest_information(self):
        session_status = "feedback"
        self.feedback_l.save_session(st.session_state.entered_code, session_status)
        st.session_state.finish_questionnaire_s = False
        st.write("Vielen Dank")
        st.button("Show feedback", on_click=self.feedback_l.user_profile_status)
    
    def show_feedback(self):
        st.write("feedback")
        info, fig = self.feedback_l.get_feedback()
        st.write(str(info))
        st.plotly_chart(fig)
        html = self.feedback_l.check_file_exist()
        if html == False:
            html = self.feedback_l.feedback_to_pdf()
        st.button("Export Report", key="export_as_pdf")
        if st.session_state.export_as_pdf:
            st.markdown(html, unsafe_allow_html=True)
                
        st.button("home", on_click=self.feedback_l.home_page_status)

    