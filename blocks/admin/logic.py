import streamlit as st
from blocks.admin.data import Admin_data
import numpy as np
import base64

import uuid
from datetime import date,datetime

class Admin_logic:

    def __init__(self):
        self.admin_d = Admin_data()

    def check_admin_cred(self):
        row = self.admin_d.get_row("Admins", st.session_state.admin_start_page_f_login, "Login")
        if row != False:
            if row[1] == st.session_state.admin_start_page_f_password:
                st.session_state.admin_menu_s = True
            else:
                st.error("Passwort ist inkorrekt")
                st.session_state.admin_start_page_s = True
        else:
            st.error("Kein Login gefunden")
            st.session_state.admin_start_page_s = True

    def admin_menu_codes_status(self):
        st.session_state.menu_codes_search_f_code = ""
        st.session_state.admin_generate_code = False
        st.session_state.admin_menu_codes_s = True
        st.session_state.search_code_s = False

    def admin_menu_edit_status(self):
        st.session_state.admin_menu_edit_s = True

    def admin_menu_download_status(self):
        st.session_state.search_download_s = False
        st.session_state.admin_menu_download_s = True
    
    def get_dataframe(self, table_name):
        return self.admin_d.get_dataframe(table_name)
    
    def save_changes(self, edited_df):
        if st.session_state.admin_menu_codes_s == True:
            self.admin_d.modify_table(edited_df, "Codes")
        elif st.session_state.admin_menu_edit_s == True:
            self.admin_d.modify_table(edited_df, "Questions")
        elif st.session_state.admin_menu_download_s == True:
            self.admin_d.modify_table(edited_df, "Users")

    def create_download_link(self, val, filename):
        b64 = base64.b64encode(val)
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


    def get_df_download(self):
        df = self.get_dataframe("Feedback_files")
        links = df["Pdf_link"].to_list()
        df= df.drop("Pdf_link", axis=1)
        
        download_links = []
        for i, pdf_data in enumerate(links):
            download_link = self.create_download_link(pdf_data, "Feedback")
            download_links.append(download_link)

        df["Pdf_link"] = download_links
        return df

    def get_df_users(self):
        df = self.get_dataframe("Users")
        return df
    def home_page_status(self):
        st.session_state.search_code_s = False
        st.session_state.start_page_s = True
        st.session_state.admin_menu_codes_s = False
        st.session_state.admin_menu_edit_s = False
        st.session_state.admin_menu_download_s = False

    def generate_code_status(self):
        st.session_state.search_code_s = False
        st.session_state.admin_menu_codes_s = False
        st.session_state.admin_generate_code = True
    
    def generate_code(self):
        for _ in range(st.session_state.enter_code_pass_f_number_of_codes):
            generated_codes = self.admin_d.get_col_list("Codes", "Code")
            code = str(uuid.uuid4().hex)[:10]
            while (code in generated_codes):
                code = str(uuid.uuid4().hex)[:10]
            today = datetime.strptime(date.today().strftime('%d.%m.%Y'), "%d.%m.%Y") 
            status = "generiert"
            self.admin_d.insert_code(code, today, status)
        
        if st.session_state.enter_code_pass_f_number_of_codes == 1:
            st.success('Der Code wurde generiert.')
        else:
            st.success('Die codes wurden generiert.')

    def search_codes_status(self):
        st.session_state.search_code = st.session_state.codes_search_f_code
        st.session_state.admin_menu_codes_s = False
        st.session_state.search_code_s = True
        
    def search_download_status(self):
        st.session_state.search_code = st.session_state.codes_search_f_code
        st.session_state.admin_menu_download_s = False
        st.session_state.search_download_s = True

    def search_code(self, code):
        result_row = self.admin_d.get_row_cond("Codes", code, "Code")
        return result_row
        
    def save_row(self, df):
        row = df.iloc[0, :].tolist()
        columns = ['Kaufdatum', 'Status']
        values = [row[1], row[2]]
        cond_val = row[0]
        self.admin_d.update_row("Codes", columns, values, "Code", cond_val)

    def search_download(self, code):
        row_files = self.admin_d.get_row_cond("Feedback_files", code, "Code")
        row_users = self.admin_d.get_row_cond("Users", code, "Code")
        links = row_files["Pdf_link"].to_list()
        row_files= row_files.drop("Pdf_link", axis=1)
        
        download_links = []
        for i, pdf_data in enumerate(links):
            download_link = self.create_download_link(pdf_data, "Feedback")
            download_links.append(download_link)

        row_files["Pdf_link"] = download_links
        result_row = row_users.merge(row_files, on='Code')
        return result_row
    
    def admin_menu_status(self):
        st.session_state.search_code_s = False
        st.session_state.admin_menu_codes_s = False
        st.session_state.admin_menu_edit_s = False
        st.session_state.admin_menu_download_s = False
        st.session_state.admin_menu_s = True