import streamlit as st
from blocks.code.ui import Code
from blocks.questionnaire.ui import Questionnaire
from blocks.feedback.ui import Feedback
from blocks.user.ui import User
from blocks.admin.ui import Admin

if "start_page_s" not in st.session_state:
    st.session_state.start_page_s = True

if "enter_code_s" not in st.session_state:
    st.session_state.enter_code_s = False

if "enter_code_password_s" not in st.session_state:
    st.session_state.enter_code_password_s = False
    
if "buy_code_s" not in st.session_state:
    st.session_state.buy_code_s = False

if "code_payment_s" not in st.session_state:
    st.session_state.code_payment_s = False

if "check_code_result_s" not in st.session_state:
    st.session_state.check_code_result_s = False

if "questionnaire_s" not in st.session_state:
    st.session_state.questionnaire_s = False

if "question_number" not in st.session_state:
    st.session_state.question_number = 0

if "demographic_vars_s" not in st.session_state:
    st.session_state.demographic_vars_s = False

if "finish_questionnaire_s" not in st.session_state:
    st.session_state.finish_questionnaire_s = False

if "user_profile_s" not in st.session_state:
    st.session_state.user_profile_s = False   

if "admin_start_page_s" not in st.session_state:
    st.session_state.admin_start_page_s = False   

if "admin_menu_s" not in st.session_state:
    st.session_state.admin_menu_s = False  

if "admin_menu_codes_s" not in st.session_state:
    st.session_state.admin_menu_codes_s = False  

if "admin_menu_edit_s" not in st.session_state:
    st.session_state.admin_menu_edit_s = False  

if "admin_menu_download_s" not in st.session_state:
    st.session_state.admin_menu_download_s = False

if "admin_generate_code" not in st.session_state:
    st.session_state.admin_generate_code = False

if "search_code_s" not in st.session_state:
    st.session_state.search_code_s = False

if "search_download_s" not in st.session_state:
    st.session_state.search_download_s = False

app_code = Code()
app_questionnaire = Questionnaire()
app_user = User()
app_feedback = Feedback()
app_admin = Admin()


# show start page

if st.session_state.start_page_s == True:
    app_code.start_page_display()

if st.session_state.buy_code_s == True:
    app_code.buy_code()

if st.session_state.enter_code_s == True:
    app_code.enter_code()

if st.session_state.enter_code_password_s == True:
    app_code.enter_code_password()
    
if st.session_state.code_payment_s == True:
    app_code.code_payment()

if st.session_state.check_code_result_s == True:
    app_code.code_information()

if st.session_state.questionnaire_s == True:
    app_questionnaire.show_question()

if st.session_state.demographic_vars_s == True:
    app_user.demographic_vars_input()

if st.session_state.finish_questionnaire_s == True:
    app_feedback.show_end_quest_information()

if st.session_state.user_profile_s == True:
    app_feedback.show_feedback()

if st.session_state.admin_start_page_s == True:
    app_admin.admin_start_page_display()

if st.session_state.admin_menu_s == True:
    app_admin.show_admin_menu()

if st.session_state.admin_menu_codes_s == True:
    app_admin.admin_menu_codes()

if st.session_state.admin_menu_edit_s == True:
    app_admin.admin_menu_edit()

if st.session_state.admin_menu_download_s == True:
    app_admin.admin_menu_download()

if st.session_state.admin_generate_code == True:
    app_admin.admin_generate_code()
    
if st.session_state.search_code_s == True:
    app_admin.admin_search_codes()

if st.session_state.search_download_s == True:
    app_admin.admin_search_download()
