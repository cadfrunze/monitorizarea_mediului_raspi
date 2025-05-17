import os
from dotenv import load_dotenv
import mariadb
from found_ip import IpRaspi


class DbAccess:
    """
    Clasa DbAccess este responsabila pentru conectarea la baza de date MariaDB (Raspbery Pi) 
    si obtinerea adresei IP de la Raspberry Pi din clasa IpRaspi (modul found_ip)
    """
    def __init__(self):
        ip_raspi: IpRaspi = IpRaspi()
        self.__ip: str = ip_raspi.get_ip()
        # incarca virtual env de la .env file
        load_dotenv()
        self.user: str = os.getenv("USER_DB")
        self.password: str = os.getenv("PASS_DB")
        self.database: str = os.getenv("DB_NAME")
        self.conn: mariadb.Connection = self.connection()

    def get_ip(self)->str:
        """
        Returneaza adresa IP a Raspberry Pi
        """
        return self.__ip

    def connection(self)-> None | mariadb.Connection:
        """Connect to database"""
        try:
            conn = mariadb.connect(
              user=os.getenv("USER_DB"),
              password=os.getenv("PASS_DB"),
              host=self.__ip,
              database=os.getenv("DB_NAME")
              )
        except mariadb.Error as e:
            raise e
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
    
    def fetch_days(self)->None | list:
        """Citeste/extrageaza zilele din baza de date"""
        self.enforce_connection()
        if self.conn is None:
            raise "Eroare la conectarea la baza de date"
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT day FROM sensor_data")
            rows = cursor.fetchall()
        days: list[str] = [row[0] for row in rows]
        return days
    
    def fetch_hours(self, day: str)->None | list:
        """Citeste/extrage intervalul orar din baza de date"""
        self.enforce_connection()
        if self.conn is None:
            raise "Eroare la conectarea la baza de date"
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT hour FROM sensor_data WHERE day = ?", (day,))
            rows = cursor.fetchall()
        hours: list[str] = [row[0] for row in rows]
        return hours
    
    def fetch_data(self, day1: str, hour1: str, day2:str , hour2: str)->None | dict:
        """Citeste/extrageaza temp, umiditatea, presiunea aer din baza de date"""
        self.enforce_connection()
        if self.conn is None:
            raise "Eroare la conectarea la baza de date"
        all_data: dict = dict()
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT temperature FROM sensor_data WHERE day BETWEEN ? AND ? AND hour BETWEEN ? AND ?", (day1, day2, hour1, hour2))
            rows_temp = cursor.fetchall()
            cursor.execute("SELECT humidity FROM sensor_data WHERE day BETWEEN ? AND ? AND hour BETWEEN ? AND ?", (day1, day2, hour1, hour2))
            rows_hum = cursor.fetchall()
            cursor.execute("SELECT pressure FROM sensor_data WHERE day BETWEEN ? AND ? AND hour BETWEEN ? AND ?", (day1, day2, hour1, hour2))
            rows_pres = cursor.fetchall()
        all_data["temperature"] = [row[0] for row in rows_temp]
        all_data["humidity"] = [row[0] for row in rows_hum]
        all_data["pressure"] = [row[0] for row in rows_pres]
        return all_data

data: DbAccess = DbAccess()
print(data.fetch_data(
    "17-05-2025",
    "01:29:59",
    "17-05-2025",
    "06:30:00"
    ))



