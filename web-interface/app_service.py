from model.all_data import AllData
from model.raspi import get_info_raspi



class AppService:
    """
    Clasa AppService este responsabila pentru gestionarea/cerintele aplicatiei.
    """
    def __init__(self):
        self.__all_data: AllData = AllData()
        self.__info_raspi: dict[str, str] = get_info_raspi()
    
    def get_info(self) -> dict[str, str]:
        """
        Returneaza adresa IP/Ssid de la Raspberry Pi
        """
        return self.__info_raspi


app: AppService = AppService() 
print(app.get_info())