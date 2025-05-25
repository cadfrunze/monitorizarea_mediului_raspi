from model.all_data import AllData
from model.raspi import RaspiSsh
import time
import matplotlib
matplotlib.use('Agg') # Fara incarcare interactiva a ferestrei
import matplotlib.pyplot as plt
import os
from flask import current_app




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
    
    def get_all_data(self, day1: str, hour1: str, day2: str, hour2: str) -> None:
        """
        Returneaza intervalul de date din baza de date.
        """
        all_data: dict = self.__all_data.data_range(day1, hour1, day2, hour2)
        inaltime: int  = 0
        # print(all_data)
        fig, axs = plt.subplots(3, 1, figsize=(max(8, min(len(all_data["hour"]) * 0.8, 30)), 8), sharex= True)
        
        # Grafic pentru temperatura
        axs[0].plot(all_data["hour"], all_data["temperature"], label="Temperatura", color="red")
        axs[0].set_ylabel("Temperatura (°C)")
        axs[0].set_xlabel("Ora")
        axs[0].set_title("Grafic temperatura")
        axs[0].grid(True)
        axs[0].legend()
        # Grafic pentru umiditate
        axs[1].plot(all_data["hour"], all_data["humidity"], label="Umiditate", color="blue")
        axs[1].set_ylabel("Umiditate (%)")
        axs[1].set_xlabel("Ora")
        axs[1].set_title("Grafic umiditate")
        axs[1].grid(True)
        axs[1].legend()
        # Grafic pentru presiune
        axs[2].plot(all_data["hour"], all_data["pressure"], label="Presiune", color="green")
        axs[2].set_ylabel("Presiune (hPa)")
        axs[2].set_xlabel("Ora")
        axs[2].set_title("Grafic presiune")
        axs[2].grid(True)
        axs[2].legend()
        # fig.legend(loc='upper right')
        
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.suptitle(
            t=f"{day1} ora {hour1} - {day2} ora {hour2}",
            fontsize=16, 
            fontweight='bold', 
            y=1,
            )
        static_path: str = os.path.join(current_app.root_path, 'static', 'grafic_sensori.png')
        plt.savefig(static_path, dpi=300)
        # print("Grafic salvat:", os.path.exists(path))
        # print("Cale fișier:", path)
        plt.close(fig)
       