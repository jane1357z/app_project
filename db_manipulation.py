import pyodbc
import pandas as pd
from sqlalchemy import create_engine

def init_connection(df=False):
    if df == True:
        connection_string = "mssql+pyodbc:///?odbc_connect=" + \
        "DRIVER={ODBC Driver 17 for SQL Server};" \
        "Server=localhost\\SQLEXPRESS;" \
        "Database=Attempt_database;" \
        "Trusted_Connection=yes;"\
        "charset=UTF8;"

        engine = create_engine(connection_string)

        conn = engine.connect()
    else:
        connection_string = "DRIVER={SQL Server};Server=localhost\\SQLEXPRESS;Database=Attempt_database;Trusted_Connection=True;"
        conn = pyodbc.connect(connection_string)
    return conn


def create_table(query):
    try:
        conn = init_connection()

        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

def insert_row(columns, row_data, table_name):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        q_val = ""
        q_val = ", ".join(["?"] * len(row_data)) 
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({q_val})"

        cursor.execute(query, row_data)
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()


def get_dataframe(table_name):
    try:
        conn = init_connection(df=True)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def single_query(query):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def delete_table(table_name):

    try:
        conn = init_connection()
        cursor = conn.cursor()
        cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")
        conn.commit()
        print(f"Table {table_name} deleted successfully.")

    except Exception as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        conn.close()

def delete_all_rows(table_name):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name}"

        cursor.execute(query)
        conn.commit()

        print(f"All rows from {table_name} deleted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()


def delete_row(id, table_name):
    try:
        conn = init_connection()
        cursor = conn.cursor()

        query = f"""DELETE from {table_name} where id_user = {id}"""

        cursor.execute(query)
        conn.commit()
        print(f"Row {id} deleted successfully.")

    except Exception as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        conn.close()


####################################################
# Create tables
####################################################

# Codes
query = '''CREATE TABLE Codes (
        Code VARCHAR(20) PRIMARY KEY,
        Kaufdatum DATE NOT NULL,
        Status NVARCHAR(255) NOT NULL);'''
# create_table(query)

# Users
query = '''CREATE TABLE Users (
            Code VARCHAR(20) PRIMARY KEY,
            Datum DATE NOT NULL,
            [Indiv. PW] NVARCHAR(20) NOT NULL,
            Name NVARCHAR (20),
            Vorname NVARCHAR (20),
            [Alter] VARCHAR(20),
            Geschlecht VARCHAR(20),
            Berufserfahrung VARCHAR(20));'''
# create_table(query)

# Questions
query = '''CREATE TABLE Questions (
        Bez NVARCHAR(255) PRIMARY KEY,
        Inhalt NVARCHAR(255) NOT NULL,
        Kategorie NVARCHAR(255) NOT NULL);'''
# create_table(query)

# example options
query = '''CREATE TABLE Example_options (
        id INT IDENTITY(1,1) PRIMARY KEY,
        Question NVARCHAR(255) NOT NULL,
        Suboption1 NVARCHAR(255) NOT NULL,
        Suboption2 NVARCHAR(255) NOT NULL,
        Suboption3 NVARCHAR(255) NOT NULL,
        Suboption4 NVARCHAR(255) NOT NULL,
        Suboption5 NVARCHAR(255) NOT NULL,
        Suboption6 VARCHAR(255) NOT NULL,
        Suboption7 VARCHAR(255) NOT NULL,
        Suboption8 VARCHAR(255) NOT NULL,
        Suboption9 VARCHAR(255) NOT NULL,
        Suboption10 VARCHAR(255) NOT NULL);'''
# create_table(query)

# users answers
query = '''CREATE TABLE Users_answers (
        id INT IDENTITY(1,1) PRIMARY KEY,
        Code VARCHAR(255) NOT NULL,
        Question_id VARCHAR(255) NOT NULL,
        Suboption1 VARCHAR(255) NOT NULL,
        Suboption2 VARCHAR(255) NOT NULL,
        Suboption3 VARCHAR(255) NOT NULL,
        Suboption4 VARCHAR(255) NOT NULL,
        Suboption5 VARCHAR(255) NOT NULL,
        Suboption6 VARCHAR(255) NOT NULL,
        Suboption7 VARCHAR(255) NOT NULL,
        Suboption8 VARCHAR(255) NOT NULL,
        Suboption9 VARCHAR(255) NOT NULL,
        Suboption10 VARCHAR(255) NOT NULL);'''
# create_table(query)

# Feedback
query = '''CREATE TABLE Feedback (
        Code VARCHAR(255) PRIMARY KEY,
        Average VARCHAR(255) NOT NULL);'''
# create_table(query)

# session
query = '''CREATE TABLE Example_Session (
        Code VARCHAR(255) PRIMARY KEY,
        Session_status VARCHAR(255) NOT NULL);'''
# create_table(query)

# Feedback_files
query = '''CREATE TABLE Feedback_files (
        Code VARCHAR(255) PRIMARY KEY,
        Pdf_link VARBINARY(MAX));'''
# create_table(query)

# Admins
query = '''CREATE TABLE Admins (
        Login VARCHAR(255) PRIMARY KEY,
        Password VARCHAR(255) NOT NULL);'''
# create_table(query)

####################################################
# Insert rows

# example_options_list = [['Ich bin.... 1','subq 1','subq 2', 'subq 3', "subq 4", "subq 5", 'subq 6','subq 7', 'subq 8', "subq 9", "subq 10"], ['Ich bin.... 2','subq A','subq B', 'subq C', "subq D", "subq E", 'subq F','subq G', 'subq H', "subq I", "subq J"]]
# columns = 'Question, Suboption1, Suboption2, Suboption3, Suboption4, Suboption5, Suboption6, Suboption7, Suboption8, Suboption9, Suboption10'

# for el in example_options_list:
#     row_data = tuple(el) 
#     insert_row(columns, row_data, 'Example_options')

# for i in range(3, 11):
#     example_options_list = [[f'Ich bin.... {str(i)}','subq 1','subq 2', 'subq 3', "subq 4", "subq 5", 'subq 6','subq 7', 'subq 8', "subq 9", "subq 10"]]
#     columns = 'Question, Suboption1, Suboption2, Suboption3, Suboption4, Suboption5, Suboption6, Suboption7, Suboption8, Suboption9, Suboption10'

#     for el in example_options_list:
#         row_data = tuple(el) 
#         insert_row(columns, row_data, 'Example_options')

# el = ["admin1", "123456"]
# columns = 'Login, Password'

# row_data = tuple(el) 
# insert_row(columns, row_data, 'Admins')
####################################################
# Get dataframe
####################################################

# df_c = get_dataframe("Codes")
# df_u = get_dataframe("Users")
# df_q = get_dataframe("Questions")
# df_o = get_dataframe("Example_options")
# df_ua = get_dataframe("Users_answers")
# df_f = get_dataframe("Feedback")
# df_s = get_dataframe("Example_Session")
# df_p = get_dataframe("Feedback_files")
# df_a = get_dataframe("Admins")
