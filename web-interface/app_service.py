from model.all_data import AllData
from model.raspi import get_info_raspi, RaspiSsh
import time



class AppService:
    """
    Clasa AppService este responsabila pentru gestionarea/cerintele aplicatiei.
    """
    def __init__(self):
        self.__all_data: AllData = AllData()
        self.__info_raspi: dict[str, str] = get_info_raspi()
        self.raspi_ssh: RaspiSsh = RaspiSsh()
    
    def get_info(self) -> dict[str, str]:
        """
        Returneaza adresa IP/Ssid de la Raspberry Pi
        """
        return self.__info_raspi
    
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


app: AppService = AppService() 
app.run_script()