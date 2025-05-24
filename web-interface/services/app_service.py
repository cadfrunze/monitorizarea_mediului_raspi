from model.all_data import AllData
from model.raspi import RaspiSsh
import time



class AppService:
    """
    Clasa AppService este responsabila pentru gestionarea/cerintele aplicatiei.
    """
    def __init__(self):
        self.__all_data: AllData = AllData()
        self.raspi_ssh: RaspiSsh = RaspiSsh()
    
    
    def run_script(self) -> None:
        """
        Ruleaza scriptul de pe Raspberry Pi pentru a citi datele de la senzori
        """
        count: int = 0
        while count < 3:
            self.raspi_ssh.run_script()
            count += 1
            if count == 3:
                self.raspi_ssh.stop_script()
            time.sleep(2)


    def get_days(self) -> list[str]:
        """
        Returneaza lista de zile din baza de date.
        """
        return self.__all_data.days()
    
    def get_hours(self, day: str) -> list[str]:
        """
        Returneaza lista de ore pentru o zi data.
        """
        return self.__all_data.hours(day)