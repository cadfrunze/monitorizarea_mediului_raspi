import mariadb
import os
from dotenv import load_dotenv


class Dbaccess:
    """Database"""
    def __init__(self):
        load_dotenv()
        self.conn = self.connection()
        
    
    def connection(self)->None | mariadb.Connection:
        """Connect to database"""
        try:
            conn = mariadb.connect(
              user=os.getenv("DB_USER"),
              password=os.getenv("DB_PASSWORD"),
              host=os.getenv("DB_HOST"),
              database=os.getenv("DB_NAME")
              )
        except mariadb.Error as e:
            print(f"Eroare la conectare: {e}")
            return None
        else:
            return conn
    
    def enforce_connection(self)->mariadb.Connection:
        """Reconectarea la baza de date!"""
        try:
            if self.conn is None:
                self.conn = self.connection()
            else:
                self.conn.ping(reconnect=True)
        except Exception as e:
            self.conn = self.connection()

        
    def insert_element(self,*args: float | str)->None:
        """Insert data"""
        self.enforce_connection()
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO sensor_data (temperature, humidity, pressure, hour, day) VALUES (?, ?, ?, ?, ?);",
                           args)
            conn.commit()




