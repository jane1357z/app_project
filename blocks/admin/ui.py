import streamlit as st
from blocks.admin.logic import Admin_logic

class Admin:
    def __init__(self):
        self.admin_l = Admin_logic()

    def admin_start_page_display(self):
        st.session_state.admin_start_page_s = False
        st.write("Admin Startseite")
        placeholder = st.empty()
        with placeholder.form(key="admin_start_page_f", border=False):
            st.text_input("Login", key ="admin_start_page_f_login")
            st.text_input("Passwort", key ="admin_start_page_f_password")
            st.form_submit_button('Weiter', on_click=self.admin_l.check_admin_cred)
        st.button("Startseite", on_click=self.admin_l.home_page_status)

    def show_admin_menu(self):
        st.session_state.admin_menu_s = False
        st.write("Admin Menu")
        st.button('Admin', on_click=self.admin_l.admin_menu_codes_status)
        st.button("Überarbeitung", on_click=self.admin_l.admin_menu_edit_status)
        st.button("Download", on_click=self.admin_l.admin_menu_download_status)

    def admin_menu_download(self):
        placeholder = st.empty()
        with placeholder.form(key="menu_codes_search_f", border=False):
            st.text_input("Search Code", key ="codes_search_f_code")
            st.form_submit_button('Search', on_click=self.admin_l.search_download_status)
    
        df_files = self.admin_l.get_df_download()
        df_users = self.admin_l.get_df_users()
        df_merged = df_users.merge(df_files, on='Code')

        html_table_begin = f"""<table>
            <tr>
                <th>Code</th>
                <th>Datum</th>
                <th>Indiv. PW</th>
                <th>Name</th>
                <th>Vorname</th>
                <th>Pdf_link</th>
            </tr>
            """
        rows_html=""""""
        for i in range(len(df_merged)):
            rows_html += f"""<tr>
                <td>{df_merged["Code"][i]}</td>
                <td>{df_merged["Datum"][i]}</td>
                <td>{df_merged["Indiv. PW"][i]}</td>
                <td>{df_merged["Name"][i]}</td>
                <td>{df_merged["Vorname"][i]}</td>
                <td>{df_merged["Pdf_link"][i]}</td>
            </tr>
            """
        html_table = html_table_begin + rows_html + """</table>"""

        st.markdown(html_table, unsafe_allow_html=True)
        st.button("Admin Menu", on_click=self.admin_l.admin_menu_status)
        st.button("Startseite", on_click=self.admin_l.home_page_status)

    def admin_menu_edit(self):
        df = self.admin_l.get_dataframe("Questions")
        edited_df = st.data_editor(df,num_rows="dynamic",  hide_index=True)
        st.button("Speichern", on_click=self.admin_l.save_changes, args = [edited_df])
        st.button("Admin Menu", on_click=self.admin_l.admin_menu_status)
        st.button("Startseite", on_click=self.admin_l.home_page_status)
    
    def admin_menu_codes(self):
        placeholder = st.empty()
        with placeholder.form(key="menu_codes_search_f", border=False):
            st.text_input("Search Code", key ="codes_search_f_code")
            st.form_submit_button('Search', on_click=self.admin_l.search_codes_status)
    
        df = self.admin_l.get_dataframe("Codes")
        edited_df = st.data_editor(df,num_rows="dynamic", disabled=["Code"], hide_index=True)
        st.button("Speichern", on_click=self.admin_l.save_changes, args = [edited_df])
        st.button("Generieren", on_click=self.admin_l.generate_code_status)
        st.button("Admin Menu", on_click=self.admin_l.admin_menu_status)
        st.button("Startseite", on_click=self.admin_l.home_page_status)
            
    def admin_generate_code(self):
        placeholder = st.empty()
        with placeholder.form(key="admin_generate_code_f", border=False):
            st.text_input("Email", key ="admin_generate_code_f_email")
            st.number_input("Anzahl Codes", value=None, step = 1, key="enter_code_pass_f_number_of_codes")
            st.form_submit_button('Generate', on_click=self.admin_l.generate_code)
        st.button("Zurück", on_click=self.admin_l.admin_menu_codes_status)

    def admin_search_codes(self):
        df = self.admin_l.search_code(st.session_state.search_code)
        if df.empty !=True:
            edited_df = st.data_editor(df,num_rows=1, disabled=["Code"], hide_index=True)
            st.button("Speichern", on_click=self.admin_l.save_row, args = [edited_df])
            st.button("Zurück", on_click=self.admin_l.admin_menu_codes_status)

        else:
            st.info("Kein Code wurde gefunden")
            st.session_state.search_code_s = False
            st.button("Zurück", on_click=self.admin_l.admin_menu_codes_status)

    def admin_search_download(self):
        df = self.admin_l.search_download(st.session_state.search_code)
        if df.empty !=True:
            html_table_begin = f"""<table>
                <tr>
                    <th>Code</th>
                    <th>Datum</th>
                    <th>Indiv. PW</th>
                    <th>Name</th>
                    <th>Vorname</th>
                    <th>Pdf_link</th>
                </tr>
                """
            rows_html=""""""
            for i in range(len(df)):
                rows_html += f"""<tr>
                    <td>{df["Code"][i]}</td>
                    <td>{df["Datum"][i]}</td>
                    <td>{df["Indiv. PW"][i]}</td>
                    <td>{df["Name"][i]}</td>
                    <td>{df["Vorname"][i]}</td>
                    <td>{df["Pdf_link"][i]}</td>
                </tr>
                """
            html_table = html_table_begin + rows_html + """</table>"""

            st.markdown(html_table, unsafe_allow_html=True)

            st.button("Startseite", on_click=self.admin_l.home_page_status)
            st.button("Zurück", on_click=self.admin_l.admin_menu_download_status)

        else:
            st.info("Kein Code wurde gefunden")
            st.session_state.search_download_s = False
            st.button("Zurück", on_click=self.admin_l.admin_menu_download_status)