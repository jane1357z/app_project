import pandas as pd
import pyodbc
from sqlalchemy import create_engine, VARCHAR, DATE, NVARCHAR

class Admin_data:
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


    def get_dataframe(self, table_name):
        if table_name == "Codes":
            query = f"""SELECT 
                    Code,
                    Kaufdatum,
                    Status 
                    FROM {table_name}"""
            # FORMAT(Kaufdatum, 'dd.MM.yyyy') AS Kaufdatum,
        elif table_name == "Questions":
            query = f"""SELECT 
                    Bez,
                    Inhalt,
                    Kategorie 
                    FROM {table_name}"""
        elif table_name == "Users":
            query = f"""SELECT 
                    Code,
                    Datum,
                    [Indiv. PW],
                    Name,
                    Vorname,
                    [Alter],
                    Geschlecht,
                    Berufserfahrung
                    FROM {table_name}"""
        elif table_name == "Feedback_files":
            query = f"""SELECT 
                    Code,
                    Pdf_link
                    FROM {table_name}"""
        try:
            conn = self.init_connection(df=True)

            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()


    def modify_table(self, edited_df, table_name):
        try:
            if table_name == "Codes":
                dtypes = {"Code": VARCHAR, "Kaufdatum": DATE, "Status": NVARCHAR}
            elif table_name == "Users":
                dtypes = {"Code": VARCHAR, "Kaufdatum": DATE, "[Indiv. PW]": NVARCHAR, "Name": NVARCHAR, "Download": VARCHAR,}
            elif table_name == "Questions":
                dtypes = {"Bez": NVARCHAR, "Inhalt":NVARCHAR, "Kategorie": NVARCHAR}
            conn = self.init_connection(True)
            edited_df.to_sql(table_name, conn, index=False, if_exists='replace', dtype=dtypes)
            
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()
    
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

    def get_col_list(self, table_name, col_name):
        df = self.get_dataframe(table_name)
        return df[col_name].to_list()
    
    def insert_code(self, code, date_, status):
        row_data = (code, date_, status)
        columns = 'Code, Kaufdatum, Status'
        table_name = "Codes"
        self.insert_row(columns, row_data, table_name)

    def get_row_cond(self, table_name, code, col):

        conn = self.init_connection(df=True)
        query = f"SELECT * FROM {table_name} WHERE {col} = '{code}';"
        result = pd.read_sql(query, conn)
        return result
        
    def update_row(self, table_name, columns, values, cond_col, cond_val):
        query = f"UPDATE {table_name} SET {columns[0]} = '{values[0]}', {columns[1]} = '{values[1]}' WHERE {cond_col} = '{cond_val}';"
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

    def get_row(self, table_name, code, col):

        conn = self.init_connection(df=True)
        query = f"SELECT * FROM {table_name} WHERE {col} = '{code}';"
        result = pd.read_sql(query, conn)
        if result.empty ==True:
            return False
        else:
            return result.iloc[0].tolist()