import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from services.app_service import AppService
import os
import socket
from datetime import datetime

class TestAppService(unittest.TestCase):
    def setUp(self):
        # Initializeaza aplicatia Flask si serviciul pentru fiecare test
        self.app = Flask(__name__)
        self.service = AppService(self.app)

    def test_make_qrcode(self):
        # Testeaza generarea codului QR
        hostname: str = socket.gethostname()
        #print(f"Hostname: {hostname}")
        local_ip:str = socket.gethostbyname(hostname)
        self.service.make_qrcode(f"http://{local_ip}:5000")
        static_path = os.path.join(self.app.root_path, 'static', 'web_adress', 'qr_code.png')
        self.assertTrue(os.path.isfile(static_path), "Codul QR ar trebui să fie generat și salvat.")

    def test_web_adress(self):
        # Testeaza generarea adresei web si a codului QR
        self.service.web_adress()
        self.assertTrue(self.service.ip_local.startswith("http://"), "Adresa IP locală trebuie să fie generată corect.")

    def test_get_all_data(self):
        # Testeaza metoda get_all_data pentru a verifica daca ruleaza fara erori
        # Aici presupunem că metoda get_all_data este implementata corect în AppService
        # si ca nu ar trebui să arunce exceptii pentru datele valide.
        try:
            self.service.get_all_data("01-06-2025", 0 , "03-06-2025", 23)
            test_passed = True
        except Exception as e:
            print(f"Error during get_all_data: {e}")
            test_passed = False
        self.assertTrue(test_passed, "Metoda get_all_data ar trebui să ruleze fără erori.")
    
    @patch('services.app_service.AllData')
    def test_get_all_data_with_mock(self, MockAllData):
        """ Testeaza metoda get_all_data cu un mock pentru AllData
        Aceasta verifica daca metoda returneaza None atunci când datele nu sunt disponibile.
        În acest caz, metoda data_range este apelata cu parametrii specificati. 
        """
        mock_instance = MockAllData.return_value
        mock_instance.data_range.return_value = {
            "temp": [(0, 22.1), (1,22.3), (2, 22.5)],
            "hum": [(0, 45), (1, 46), (2, 47)],
            "press": [(0,1012), (1,1013), (2,1011)]
        }
        service = AppService(app=self.app)
        result = service.get_all_data("01-06-2025", 0, "02-06-2025", 23)
        self.assertIsNone(result)
        mock_instance.data_range.assert_called_with(0, 23, "01-06-2025", "02-06-2025")


    def test_start_and_stop_script(self):
        # Testează pornirea și oprirea scriptului în fundal
        self.service.start_script()
        self.assertTrue(self.service.running, "Scriptul ar trebui să fie pornit.")
        self.service.stop_script()
        self.assertFalse(self.service.running, "Scriptul ar trebui să fie oprit.")

if __name__ == '__main__':
    # Seteaza directorul de lucru pentru a fi același cu scriptul curent
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(f'{script_dir}\\testing', 'test_appservice.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"Test pornit la date de: {datetime.now().strftime("%d/%m/%Y")} ora: {datetime.now().strftime("%H:%M:%S")}\n")
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.TextTestRunner.run = runner.run
        unittest.main(exit=False)