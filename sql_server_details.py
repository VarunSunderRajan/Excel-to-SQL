import pyodbc


def create_new_database(server, db_name, username, password):
    # Connection string to connect to the server
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};' \
               f'UID={username};PWD={password};Trusted_Connection=yes;'
    
    # Connect to the server with autocommit enabled for DDL commands
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    # SQL command to create a new database
    create_db_query = f"CREATE DATABASE {db_name};"

    # Execute the SQL command
    cursor.execute(create_db_query)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print(f"Database {db_name} created successfully.")

def get_db_connection(server, db_name, username, password):
    # Connection string to connect to the specific database
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={db_name};' \
               f'UID={username};PWD={password};Trusted_Connection=yes;'
    
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    return conn
