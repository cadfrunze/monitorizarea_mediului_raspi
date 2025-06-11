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
# Constructie a codului QR
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from PIL import Image
from io import BytesIO
import socket # pentru a obtine adresa IP a dispozitivului local





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
        # self.list_count_user: list[int] = list()
        # self.count_user: int = 0


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
    
    def get_all_data(self, day1: str, hour1: str, day2: str, hour2: str) -> None:
        """
        Returneaza intervalul de date din baza de date. Afiseaza un grafic cu datele din baza de date
        """
        all_data: dict[str, list[tuple[int, float]]] = self.__data_raspi.data_range(hour1, hour2, day1, day2)
        # Extragerea datelor pentru fiecare senzor
        data_hours: list[int] = [item[0] for item in all_data["temp"]]   # itereaza prin toate tupleurile si extrage orele din temp
        data_temp: list[float] = [round(item[-1], 1) for item in all_data["temp"]] # extrage temperatura pentru fiecare ora
        data_hum: list[float] = [item[-1] for item in all_data["hum"]]   # extrage umiditatea pentru fiecare ora
        data_press: list[float] = [item[-1] for item in all_data["press"]] # extrage presiunea pentru fiecare ora

        # print(f"data_hours = {data_hours}")
        # print(f"data_temp = {data_temp}")
        # print(f"data_hum = {data_hum}")
        # print(f"data_press = {data_press}")

        fig, axs = plt.subplots(3, 1, figsize=(max(8, min(len(data_hours) * 0.8, 30)), 8))

        # Constructia axei x pe pozitii sumerice (0, 1, 2, ...)
        axa_x: range[int] = range(len(data_hours))
        # Etichetele vor fi orele convertite în string pt a fi afișate pe axa x
        labels: list[str] = [str(h) for h in data_hours]

        # Grafic pentru temperatura
        axs[0].plot(axa_x, data_temp, label="Temperatura", color="red")
        axs[0].set_xticks(axa_x)
        axs[0].set_xticklabels(labels, rotation=45)
        axs[0].set_ylabel("°C")
        axs[0].set_xlabel("Interval Orar")
        axs[0].set_title("Temperatura")
        axs[0].grid(True)
        axs[0].legend()

        # Grafic pentru umiditate
        axs[1].plot(axa_x, data_hum, label="Umiditate Rel.", color="blue")
        axs[1].set_xticks(axa_x)
        axs[1].set_xticklabels(labels, rotation=45)
        axs[1].set_ylabel("RH (%)")
        axs[1].set_xlabel("Interval Orar")
        axs[1].set_title("Umiditate Relativa")
        axs[1].grid(True)
        axs[1].legend()

        # Grafic pentru presiune
        axs[2].plot(axa_x, data_press, label="Presiune Atm.", color="green")
        axs[2].set_xticks(axa_x)
        axs[2].set_xticklabels(labels, rotation=45)
        axs[2].set_ylabel("hPa")
        axs[2].set_xlabel("Interval Orar")
        axs[2].set_title("Presiune Atmosferica")
        axs[2].grid(True)
        axs[2].legend()

        # ajustarea aspectului graficului
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.suptitle(
            t=f"{day1} ora {hour1} - {day2} ora {hour2}",
            fontsize=16,
            fontweight='bold',
            y=1,
        )
        # Salveaza graficul in directorul static al aplicatiei Flask
        static_path: str = os.path.join(current_app.root_path, 'static', 'grafic_istoric', 'grafic_sensori.png')
        plt.savefig(static_path, dpi=300)
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
        self.list_temp.append(round(data_raspi["temp"], 1))
        self.list_hum.append(round(data_raspi["hum"], 1))
        self.list_pres.append(round(data_raspi["press"], 2))
        axa_x : range[int] = range(len(self.list_hours))
        fig, axs = plt.subplots(3, 1, figsize=(max(8, min(len(self.list_hours) * 0.8, 30)), 8))
        
        # Grafic pentru temperatura
        axs[0].plot(self.list_hours, self.list_temp, label="Temperatura", color="red")
        axs[0].set_xticks(axa_x)
        axs[0].set_xticklabels(self.list_hours, rotation=45)
        axs[0].set_ylabel("°C")
        axs[0].set_xlabel("Ora")
        axs[0].set_title("Temperatura")
        axs[0].grid(True)
        axs[0].legend()
        # Grafic pentru umiditate
        axs[1].plot(self.list_hours, self.list_hum, label="Umiditate Rel.", color="blue")
        axs[1].set_xticks(axa_x)
        axs[1].set_xticklabels(self.list_hours, rotation=45)
        axs[1].set_ylabel("RH %")
        axs[1].set_xlabel("Ora")
        axs[1].set_title("Umiditate Relativa")
        axs[1].grid(True)
        axs[1].legend()
        # Grafic pentru presiune
        axs[2].plot(self.list_hours, self.list_pres, label="Presiune Atm.", color="green")
        axs[2].set_xticks(axa_x)
        axs[2].set_xticklabels(self.list_hours, rotation=45)
        axs[2].set_ylabel("hPa")
        axs[2].set_xlabel("Ora")
        axs[2].set_title("Presiune Atmosferica")
        axs[2].grid(True)
        axs[2].legend()
        # fig.legend(loc='upper right')
        
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        static_path: str = os.path.join(current_app.root_path, 'static', 'grafic_sensors' , "grafic_raspi.png")
        plt.savefig(static_path, dpi=300)
        plt.close(fig)
    
    def make_qrcode(self, stringul: str) -> None:
        """
        Genereaza un cod QR pentru un string dat.
        """
        
        
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(stringul)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")        
        qr_buffer: BytesIO = BytesIO()
        img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        static_path: str = os.path.join(current_app.root_path, 'static', 'web_adress', 'qr_code.png')
        img.save(static_path, format="PNG")
    
    def web_adress(self)->None:
        """
        Returneaza adresa web a aplicatiei Flask.
        """
        
        hostname: str = socket.gethostname()
        local_ip:str = socket.gethostbyname(hostname)
        self.make_qrcode(f"http://{local_ip}:5000")

    
    # def delete_all_graphics(self) -> None:
    #     """
    #     Sterge toate graficele generate.
    #     """
    #     static_path: str = os.path.join(current_app.root_path, 'static')
    #     folders: list[str] = [
    #         'grafic_sensors',
    #         'grafic_istoric'
    #     ]    
    #     for folder in folders:
    #         folder_path: str = os.path.join(static_path, folder)
    #         for filename in os.listdir(folder_path):
    #             file_path: str = os.path.join(folder_path, filename)
    #             if os.path.isfile(file_path):
    #                 os.remove(file_path)
        
        
       