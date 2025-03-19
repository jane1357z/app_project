import pandas as pd
import pyodbc
from sqlalchemy import create_engine


class Feedback_data:
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
    
    def insert_average(self, code, average, table_name):
        row_data = (code, average)
        columns = 'Code, Average'
        self.insert_row(columns, row_data, table_name)

    def get_cond_dataframe(self, table_name, cond):
        try:
            conn = self.init_connection(df=True)
            
            query = f"SELECT * FROM {table_name} WHERE Code = '{cond}';"
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

    def get_col_list(self, table_name, col_name):
        df = self.get_dataframe(table_name)
        return df[col_name].to_list()
    
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
    
    def get_user_answers(self, table_name, code):
        df = self.get_cond_dataframe(table_name, code)
        return df
    
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

    def get_average_value(self, table_name, code, col):

        conn = self.init_connection(df=True)
        query = f"SELECT * FROM {table_name} WHERE {col} = '{code}';"
        result = pd.read_sql(query, conn)
        if result.empty ==True:
            return False
        else:
            return result.iloc[0]["Average"]
    
    def add_pdf(self, code, pdf_string, table_name):
        
        try:
            conn = self.init_connection()
            cursor = conn.cursor()

            query = f"INSERT INTO {table_name} (Code, Pdf_link) VALUES (?, ?)"
            
            row_data = (code, pdf_string)
            cursor.execute(query, row_data)
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def get_row(self, table_name, code, col):
        conn = self.init_connection(df=True)
        query = f"SELECT * FROM {table_name} WHERE {col} = '{code}';"
        result = pd.read_sql(query, conn)
        if result.empty ==True:
            return False
        else:
            return result.iloc[0].tolist()
        
    def get_row_cond(self, table_name, code, col):

        conn = self.init_connection(df=True)
        query = f"SELECT * FROM {table_name} WHERE {col} = '{code}';"
        result = pd.read_sql(query, conn)
        return result