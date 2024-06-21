import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class Manager:
    def __init__(self) -> None:
        self.host = os.getenv('HOST')
        self.db_name = os.getenv('DB_NAME')
        self.port = os.getenv('PORT')
        self.login = os.getenv('LOGIN')
        self.password = os.getenv('PASSWORD')
        self.conn = None
        self.cursor=None

    def get_conn(self)->None:
        try:
            self.conn = psycopg2.connect(database=self.db_name,
                                    host=self.host,
                                    user=self.login,
                                    password=self.password,
                                    port=self.port)


            print("Connection successful")
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM _user")
            rows = self.cursor.fetchall() 

            
            for row in rows:
                print(row)

        except Exception as error:
            print(f"Error: {error}")

    def close_conn(self)->None:
        if self.conn:
            self.cursor.close()
            self.conn.close()



mng = Manager()
mng.get_conn()
mng.close_conn()