from databases.db_access import DbAccess


class AllData:
    """
    Clasa AllData este responsabila pentru gestionarea datelor din baza de date.
    """
    def __init__(self):
        self.__db: DbAccess = DbAccess()
    
    
    def data_range(self, start_hour:int, end_hour:int, ziua1: str, ziua2:str) -> dict | None:
        """
        Returneaza intervalul de date din baza de date.
        """
        all_data = self.__db.get_data()
        if all_data is None:
            raise Exception("Nu s-au putut obtine datele din baza de date.")
        new_data: dict = {
            key: {
                sub_key: sub_val
                for sub_key, sub_val in values.items()
                if (start_hour <= sub_val['hour'] <= end_hour) and ziua1 == sub_val['day'] and ziua2 == sub_val['day']
                }
            for key, values in all_data.items()
        }
        return new_data

        
  
        
        
        
        


        