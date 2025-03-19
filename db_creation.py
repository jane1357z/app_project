import pyodbc

try:

    connection_string = "DRIVER={SQL Server};Server=localhost\\SQLEXPRESS;Database=master;Trusted_Connection=True;"
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE Attempt_database")

    conn.commit()
    print("Database  created successfully.")
    
    cursor.close()
    conn.close()

except pyodbc.Error as e:
    print("Error:", e)


