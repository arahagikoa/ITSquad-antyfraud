import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()


host = os.getenv('HOST')
db_name = os.getenv('DB_NAME')
port = os.getenv('PORT')
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')


try:
    conn = psycopg2.connect(database=db_name,
                            host=host,
                            user=login,
                            password=password,
                            port=port)


    print("Connection successful")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM _user")
    rows = cursor.fetchall() 

    
    for row in rows:
        print(row)

except Exception as error:
    print(f"Error: {error}")


finally:
    if conn:
        cursor.close()
        conn.close()