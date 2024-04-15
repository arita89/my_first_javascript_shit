import os
import psycopg2

def test_db_connection():
    # Environment variables
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')

    # Connection string
    conn_str = f"dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' host='{POSTGRES_HOST}' port='{POSTGRES_PORT}' password='{POSTGRES_PASSWORD}'"
    
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()

        # Execute a query
        cur.execute('SELECT VERSION()')

        # Fetch and print the result
        version = cur.fetchone()
        print(f"Database connection successful: {version[0]}")

        # Close the cursor and the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()
