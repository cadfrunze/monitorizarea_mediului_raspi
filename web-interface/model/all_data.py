from databases.db_access import DbAccess


class AllData:
    """
    Clasa AllData este responsabila pentru gestionarea datelor din baza de date.
    """
    def __init__(self):
        self.__db: DbAccess = DbAccess()
    
    def days(self) -> list:
        """
        Returneaza lista de zile din baza de date.
        """
        return self.__db.fetch_days()
    
    def hours(self, day: str) -> list:
        """
        Returneaza lista de ore din baza de date.
        """
        return self.__db.fetch_hours(day)
    
    def data_range(self, day1: str, hour1: str, day2:str , hour2: str) -> None | dict[list[str], list[str], list[str]]:
        """
        Returneaza intervalul de date din baza de date.
        """
        return self.__db.fetch_data(day1, hour1, day2, hour2)
        