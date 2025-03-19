import pandas as pd
import pyodbc
from sqlalchemy import create_engine


class User_data:
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