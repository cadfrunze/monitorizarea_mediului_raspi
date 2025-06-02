from databases.db_access import DbAccess
from datetime import datetime, timedelta

db: DbAccess = DbAccess()

class AllData:
    """
    Clasa AllData este responsabila pentru gestionarea datelor din baza de date.
    """
    def __init__(self):

        self.all_data: dict = db.get_data()
    
    
    def data_range(self, start_hour:int, end_hour:int, ziua1: str, ziua2:str) -> dict | None:
        """
        Returneaza intervalul de ore, date: temp, umidiate, presiune din date din baza de date.
        """
        
        if self.all_data is None:
            raise Exception("Nu s-au putut obtine datele din baza de date.")
        # Obtinerea intervalului de zile
        final_data: dict[str, list[tuple[int, float]]] = {
            "temp": [],
            "hum": [],
            "press": [],
            }
        interval_time: list[list[str, list[int]]] = list() # index[0] = ziua, index[1] = intervalul de ore
        interval_hours: list[int] = list()
        start_date: datetime = datetime.strptime(ziua1, "%d-%m-%Y")
        end_date: datetime = datetime.strptime(ziua2, "%d-%m-%Y")
        current_date: datetime = start_date
        while current_date <= end_date:
            interval_time.append([current_date.strftime("%d-%m-%Y")])
            current_date += timedelta(days=1)
        # Obtinerea intervalului de ore
        if ziua1 == ziua2:
            interval_time[0].append([ora for ora in range(start_hour, end_hour + 1)])
            
        else:
            for day in interval_time:
                if day == interval_time[0]:
                    day.append([ora for ora in range(start_hour, 24)])
                elif day != interval_time[0] and day != interval_time[-1]:
                    day.append([ora for ora in range(0, 24)])
                elif day == interval_time[-1]:
                    day.append([ora for ora in range(0, end_hour + 1)])
        # Obtinerea datelor din baza de date
        for time in interval_time:
            for hour in time[1]: # interatia pt intervalul de ore din ziua curenta
                for k, v in self.all_data.items(): # vezi k la iterare k va fi cheia "temp", "hum" sau "press"
                    # print(f"Key: {k}, Value: {v}")
                    for data in v.values():
                        if data["day"] == time[0] and data["hour"] == hour:
                            if k == "temp": 
                                final_data["temp"].append((hour, data["value_temp"]))
                            elif k == "hum":
                                final_data["hum"].append((hour, data["value_hum"]))
                            elif k == "press":
                                final_data["press"].append((hour, data["value_press"]))
        return final_data
        
        
        


        