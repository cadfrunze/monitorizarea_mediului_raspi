import os
from dotenv import load_dotenv
import mariadb
from found_ip import IpRaspi


class DbAccess:
    """
    Clasa DbAccess este responsabila pentru conectarea la baza de date MariaDB (Raspbery Pi) si obtinerea adresei IP de la Raspberry Pi din clasa IpRaspi (modul found_ip.py).
    """
    def __init__(self):
        ip_raspi: IpRaspi = IpRaspi()
        self.ip: str = ip_raspi.get_ip()
        # incarca virtual env de la .env file
        load_dotenv()
        self.user: str = os.getenv("USER_DB")
        self.password: str = os.getenv("PASS_DB")
        self.database: str = os.getenv("DB_NAME")
        self.conn: mariadb.Connection = self.connection()

    def connection(self)->None | mariadb.Connection:
        """Connect to database"""
        try:
            conn = mariadb.connect(
              user=os.getenv("USER_DB"),
              password=os.getenv("PASS_DB"),
              host=self.ip,
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
    
    def fetch_temp(self)->None | list:
        """Fetch temperature from database"""
        self.enforce_connection()
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM sensor_data")
            rows = cursor.fetchall()
            return rows

data: DbAccess = DbAccess()
print(data.fetch_temp())



