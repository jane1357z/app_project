import pandas as pd
import pyodbc
from sqlalchemy import create_engine


class Questionnaire_data:
    def __init__(self):
        pass
    def init_connection(self, df=False):
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

    def insert_row(self,columns, row_data, table_name):
        try:
            conn = self.init_connection()
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

    def get_dataframe(self,table_name):
        try:
            conn = self.init_connection(df=True)
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

    def get_question(self, table_name):
        df = self.get_dataframe(table_name)
        return df[df.columns[1]].to_list()
    
    def get_suboptions(self, table_name):
        df = self.get_dataframe(table_name)
        return df.iloc[:, 2:].values.tolist()
    
    def add_answers(self, code, question_id, answers):
        row_data = (code, question_id, *answers)
        columns = 'Code, Question_id, Suboption1, Suboption2, Suboption3, Suboption4, Suboption5, Suboption6, Suboption7, Suboption8, Suboption9, Suboption10'
        table_name = "Users_answers"
        self.insert_row(columns, row_data, table_name)

    def update_session(self, code, status):
        table_name = "Example_Session"
        query = f"UPDATE {table_name} SET Session_status = '{status}' WHERE Code = '{code}';"
        try:
            conn = self.init_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()