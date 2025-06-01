from model.all_data import AllData
from model.raspi import RaspiSsh
import time
import matplotlib
matplotlib.use('Agg') # Fara incarcare interactiva a ferestrei GUI tkinter
# pentru a evita erorile de import in medii fara GUI
import matplotlib.pyplot as plt
import os
from flask import current_app, Flask
import threading #pt a rula scriptul in background





class AppService:
    """
    Clasa AppService este responsabila pentru gestionarea/cerintele aplicatiei.
    """
    def __init__(self, app: Flask) -> None:
        self.app = app 
        self.running: bool = False       
        self.__data_raspi: AllData = AllData()
        self.raspi_ssh: RaspiSsh = RaspiSsh()
        self.list_hours: list[str] = list()
        self.list_temp: list[float] = list()
        self.list_hum: list[float] = list()
        self.list_pres: list[float] = list()
        self.thread: threading.Thread | None = None
        self.stop_event: threading.Event = threading.Event()
        self.list_count_user: list[int] = list()
        self.count_user: int = 0


    def start_script(self) -> None:
        """
        Porneste scriptul de pe Raspberry Pi pentru a citi datele de la senzori in fundal.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_script_raspi)
            self.thread.start()
            
    def stop_script(self) -> None:
        """
        Opreste scriptul de pe Raspberry Pi.
        """
        self.running = False
        if self.thread is not None:
            self.thread.join()
        self.list_hours.clear()
        self.list_temp.clear()
        self.list_hum.clear()
        self.list_pres.clear()
    
    
    def run_script_raspi(self) -> None:
        """
        Ruleaza scriptul de pe Raspberry Pi pentru a citi datele de la senzori
        """
        with self.app.app_context():
            while self.running:
                self.get_data_raspi()
                time.sleep(2)
        


    def get_days(self) -> list[str]:
        """
        Returneaza lista de zile din baza de date.
        """
        return self.__data_raspi.days()
    
    def get_hours(self, day: str) -> list[str]:
        """
        Returneaza lista de ore pentru o zi data.
        """
        return self.__data_raspi.hours(day)
    
    def get_all_data(self, day1: str, hour1: str, day2: str, hour2: str) -> None:
        """
        Returneaza intervalul de date din baza de date. Afiseaza un grafic cu datele din baza de date
        """
        all_data: dict[str, list[tuple[int, float]]] = self.__data_raspi.data_range(day1, hour1, day2, hour2)
        # Extragerea datelor pentru fiecare senzor
        data_hours: list[int] = [str(item[0]) for item in all_data["temp"]]
        data_temp: list[float] = [item[-1] for item in all_data["temp"]]
        data_hum: list[float] = [item[-1] for item in all_data["hum"]]
        data_press: list[float] = [item[-1] for item in all_data["press"]]

        fig, axs = plt.subplots(3, 1, figsize=(max(8, min(len(data_hours) * 0.8, 30)), 8))
        
        # Grafic pentru temperatura
        axs[0].plot(data_hours, data_temp, label="Temperatura", color="red")
        axs[0].set_xticklabels(data_hours, rotation=45)
        #axs[0].set_yticks(data_temp)
        axs[0].set_ylabel("Temperatura (°C)")
        axs[0].set_xlabel("Intervalul de ore")
        axs[0].set_title("Grafic temperatura")
        axs[0].grid(True)
        axs[0].legend()
        # Grafic pentru umiditate
        axs[1].plot(data_hours, data_hum, label="Umiditate", color="blue")
        axs[1].set_xticklabels(data_hours, rotation=45)
        axs[1].set_ylabel("Umiditate (%)")
        axs[1].set_xlabel("Intervalul de ore")
        axs[1].set_title("Grafic umiditate")
        axs[1].grid(True)
        axs[1].legend()
        # Grafic pentru presiune
        axs[2].plot(data_hours, data_press, label="Presiune", color="green")
        axs[2].set_xticklabels(data_hours, rotation=45)
        axs[2].set_ylabel("Presiune (hPa)")
        axs[2].set_xlabel("Intervalul de ore")
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
        static_path: str = os.path.join(current_app.root_path, 'static', 'grafic_istoric' , f'grafic_sensori{self.list_count_user[self.count_user - 1]}.png')
        plt.savefig(static_path, dpi=300)
        # print("Grafic salvat:", os.path.exists(path))
        # print("Cale fișier:", path)
        plt.close(fig)
    
    def get_data_raspi(self) -> None:
        """
        Returneaza datele de la Raspberry Pi. Afiseaza un grafic cu datele de la senzori.
        """
        try:
            data_raspi: dict | None = self.raspi_ssh.run_script()
        except Exception as e:
            raise Exception(f"Eroare la rularea scriptului de pe Raspberry Pi: {e}")
        self.list_hours.append(data_raspi["hour"])
        self.list_temp.append(data_raspi["temperature"])
        self.list_hum.append(data_raspi["humidity"])
        self.list_pres.append(data_raspi["pressure"])
        fig, axs = plt.subplots(3, 1, figsize=(max(8, min(len(self.list_hours) * 0.8, 30)), 8))
        
        # Grafic pentru temperatura
        axs[0].plot(self.list_hours, self.list_temp, label="Temperatura", color="red")
        axs[0].set_ylabel("Temperatura (°C)")
        axs[0].set_xlabel("Ora")
        axs[0].set_title("Grafic temperatura")
        axs[0].grid(True)
        axs[0].legend()
        # Grafic pentru umiditate
        axs[1].plot(self.list_hours, self.list_hum, label="Umiditate", color="blue")
        axs[1].set_ylabel("Umiditate (%)")
        axs[1].set_xlabel("Ora")
        axs[1].set_title("Grafic umiditate")
        axs[1].grid(True)
        axs[1].legend()
        # Grafic pentru presiune
        axs[2].plot(self.list_hours, self.list_pres, label="Presiune", color="green")
        axs[2].set_ylabel("Presiune (hPa)")
        axs[2].set_xlabel("Ora")
        axs[2].set_title("Grafic presiune")
        axs[2].grid(True)
        axs[2].legend()
        # fig.legend(loc='upper right')
        
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        static_path: str = os.path.join(current_app.root_path, 'static', 'grafic_sensors' , f"grafic_raspi{self.list_count_user[self.count_user - 1]}.png")
        plt.savefig(static_path, dpi=300)
        # print("Grafic salvat:", os.path.exists(path))
        # print("Cale fișier:", path)
        plt.close(fig)
    
    def delete_all_graphics(self) -> None:
        """
        Sterge toate graficele generate.
        """
        static_path: str = os.path.join(current_app.root_path, 'static')
        folders: list[str] = [
            'grafic_sensors',
            'grafic_istoric'
        ]    
        for folder in folders:
            folder_path: str = os.path.join(static_path, folder)
            for filename in os.listdir(folder_path):
                file_path: str = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        
       