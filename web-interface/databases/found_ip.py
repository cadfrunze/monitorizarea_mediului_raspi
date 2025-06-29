from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, db





class IpRaspi:
    """
    Clasa IpRaspi este responsabila pentru conectarea la Firebase si obtinerea adresei IP de la Raspberry Pi.
    """
    def __init__(self):
        # incarca virtual env de la .env file
        load_dotenv()
        # incarca credentialele de la firebase
        self.credentials: str = os.getenv("CREDENTIALS")
        self.endpoint: str = os.getenv("END_POINT")
        self.url: str = os.getenv("URL_ADR")
        # initializeaza firebase
           

    def connect(self)-> db.Reference | None:
        """
        Incarca credentialele de la firebase
        """
        try:
            # incarca credentialele de la firebase
            self.cred = credentials.Certificate(self.credentials)
        except Exception as e:
            raise e
        # initializeaza firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred, {
                'databaseURL': self.url
            })
        # conecteaza la baza de date
        return db.reference(f"/status/{self.endpoint}")
    
    def get_ip(self)-> str | None:
        """
        Conecteaza la baza de date si obtine adresa IP de la Raspberry Pi
        """
        ref = self.connect()
        if ref is None:
            raise ConnectionError("Eroare la conectarea la Firebase")
        ip: str = ref.child("adresa").get()
        return ip
    
    def get_ssid(self)-> str | None:
        """
        Conecteaza la baza de date si obtine SSID-ul de la Raspberry Pi
        """
        ref = self.connect()
        if ref is None:
            raise ConnectionError("Eroare la conectarea la Firebase")
        ssid: str = ref.child("retea").get()
        return ssid




