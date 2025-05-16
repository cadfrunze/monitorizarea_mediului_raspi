from all_sensors.read_data import read_temp, read_pressure, read_hum
from database.db_access import Dbaccess
from datetime import datetime



class Services:

    def __init__(self):
        self.db: Dbaccess = Dbaccess() 
    
    def add_element(self)->None:
        temp: float | None = read_temp()
        pressure: float | None = read_pressure()
        humidity: float | None = read_hum()
        time_day: str = datetime.now().strftime("%d-%m-%Y")
        time_hour: str = datetime.now().strftime("%H:%M:%S")
        self.db.insert_element(temp, pressure, humidity, time_hour, time_day)
    


        








    

