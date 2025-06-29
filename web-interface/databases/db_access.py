import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from databases.found_ip import IpRaspi


class DbAccess:
    """
    Clasa DbAccess este responsabila pentru conectarea la baza de date firebase,
    extragerea datelor din baza de date si
    obtinerea adresei IP/ssid de la Raspberry Pi din clasa IpRaspi (modul found_ip)
    """
    def __init__(self):
        ip_raspi: IpRaspi = IpRaspi()
        self.__ip: str = ip_raspi.get_ip() #private
        self.__ssid: str = ip_raspi.get_ssid() #private
        # incarca virtual env de la .env file
        load_dotenv()
        # initializeaza conexiunea la baza de date firebase
        self.__CREDENTIALS : str = os.getenv("CREDENTIALS")
        self.__URL_ADDRESS: str = os.getenv("URL_ADR")
        self.__END_POINT_DATABASE: str = os.getenv("END_POINT_DATA")
        self.connection: db.Reference | None = self.connect()
    
    def connect(self) -> db.Reference | None:
        """
        Incarca credentialele de la firebase si initializeaza conexiunea la baza de date
        """
        try:
            cred = credentials.Certificate(self.__CREDENTIALS)
        except Exception as e:
            raise e
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.__URL_ADDRESS
            })
        return db.reference(f"/status/{self.__END_POINT_DATABASE}")
    
    
    def get_ip(self)->str:
        """Returneaza adresa IP de la Raspberry Pi"""
        return self.__ip
    
    def get_ssid(self)->str:
        """Returneaza SSID-ul de la Raspberry Pi"""
        return self.__ssid
    
    def get_data(self)-> dict | None:
        """
        Conecteaza la baza de date si obtine datele de la Raspberry Pi
        """
        ref = self.connection
        if ref is None:
            raise ConnectionError("Eroare la conectarea la Firebase")
        data: dict | None = ref.get()
        return data 
    
# db_access: DbAccess = DbAccess()
# print(db_access.get_data())  # For testing purposes, prints the data fetched from Firebase
    




