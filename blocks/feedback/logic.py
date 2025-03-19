import streamlit as st
from blocks.feedback.data import Feedback_data
from fpdf import FPDF
import base64
import tempfile
import os

from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Feedback_logic:
    def __init__(self):
        self.feedback_d = Feedback_data()

    def user_profile_status(self):
        html = self.check_file_exist()
        if html == False:
            answers_df = self.feedback_d.get_user_answers("Users_answers", st.session_state.entered_code)
            opt_dict = {"o1": 1, "o2": 2, "o3": 3, "o4": 4, "o5": 5, "o6": 6, "o7": 7}
            average_per_answer = []
            for i in range(len(answers_df)):
                items = answers_df.iloc[i, 3:].tolist()
                total_sum = sum(opt_dict[item] for item in items)
                average_per_answer.append(total_sum/10) # get average 
            self.feedback_d.insert_average(st.session_state.entered_code, str(average_per_answer),"Feedback")
        st.session_state.user_profile_s = True

    def home_page_status(self):
        st.session_state.user_profile_s = False
        st.session_state.start_page_s = True

    def save_session(self, code, status):
        self.feedback_d.update_session(code, status)

    def create_download_link(self, val, filename):
        b64 = base64.b64encode(val)
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    def feedback_to_pdf(self):

        feedback_info, fig = self.get_feedback()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            fig.write_image(tmpfile.name, format="png", engine="kaleido", scale=1)
            tmpfile_path = tmpfile.name

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(20, 20, 10)
        pdf.set_font('Arial', 'B', 16)

        users_info = self.feedback_d.get_row("Users", st.session_state.entered_code, "Code")
        
        pdf.cell(0, 10, "Feedback", ln = 1, align="C")
        
        pdf.set_font('Arial','', 12)
        pdf.cell(40, 10, str(feedback_info), ln = 1)
        pdf.cell(40, 10, "Indiv. PW")
        pdf.cell(40, 10, str(users_info[2]), ln = 1)
        pdf.cell(40, 10, str(users_info[3]), ln = 1)
        pdf.cell(40, 10, str(users_info[4]), ln = 1)
        pdf.cell(40, 10, str(users_info[5]), ln = 1)

        pdf.image(tmpfile_path, x=30, y=100, w=90)

        os.remove(tmpfile_path)

        pdf_string = pdf.output(dest="S").encode("latin-1")

        self.feedback_d.add_pdf(st.session_state.entered_code, pdf_string, "Feedback_files")

        html = self.create_download_link(pdf.output(dest="S").encode("latin-1"), "Feedback")
        
        return html
    
    def get_feedback(self):
        
        feedback_average = self.feedback_d.get_average_value("Feedback", st.session_state.entered_code, "Code")
        average = [float(x) for x in feedback_average[1:-1].split(",")]
        all_average = self.feedback_d.get_col_list("Feedback", "Average")

        aver_question = [0,0]
        for el in all_average:
            average_el = [float(x) for x in el[1:-1].split(",")]
            aver_question[0] += average_el[0]
            aver_question[1] += average_el[1]
        all_aver_question = [x / len(all_average) for x in aver_question]
        categories = ["Own", "All"]
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Frage 1","Frage 2"))

        fig.add_trace(
            go.Bar(
                x=categories, 
                y=[average[0], all_aver_question[0]], 
                marker=dict(color="purple")),
            row=1, col=1 
        )

        fig.add_trace(
            go.Bar(
                x=categories, 
                y=[average[1], all_aver_question[1]],
                marker=dict(color="orange")),
            row=1, col=2 
        )

        fig.update_layout(
            title="Bar Plot Example in Subplot",
            xaxis1_title="Question",
            yaxis1_title="Average",
            xaxis2_title="Question",
            yaxis2_title="Average", 
            yaxis1=dict(range=[0, 8]),
            yaxis2=dict(range=[0, 8]),
            width=800,
            height=400, showlegend=False
        )

        return feedback_average, fig

    def check_file_exist(self):
        row_files = self.feedback_d.get_row_cond("Feedback_files", st.session_state.entered_code, "Code")
        if row_files.empty == True:
            return False
        else:
            pdf_data = row_files.iloc[0].tolist()[1]
            download_link = self.create_download_link(pdf_data, "Feedback")
            return download_link
