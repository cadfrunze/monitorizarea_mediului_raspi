import unittest
from datetime import datetime
import os
import paramiko



class TestRaspiSsh(unittest.TestCase):
    """Testele pentru clasa RaspiSsh care se ocupa cu conexiunea SSH la Raspberry Pi
    si rularea scriptului pentru citirea datelor de la senzori."""
    def test_connect(self):
        """Testeaza conexiunea SSH la Raspberry Pi"""
        from model.raspi import RaspiSsh
        raspissh = RaspiSsh()
        ref = raspissh.connect_raspi()
        self.assertIsInstance(ref, paramiko.SSHClient, "Conexiunea SSH la Raspberry Pi ar trebui sa fie stabilita")

    def test_run_script(self):
        """Testeaza rularea scriptului pe Raspberry Pi si verificarea raspunsului"""
        # Asigura-te ca ai configurat corect scriptul pe Raspberry Pi si ca acesta returneaza un dictionar cu datele de la senzori
        # In acest test, presupunem ca scriptul returneaza un dictionar cu cheile 'temp', 'hum' si 'press'
        # si valorile corespunzatoare pentru temperatura, umiditate si presiune
        from model.raspi import RaspiSsh
        raspissh = RaspiSsh()
        ref = raspissh.run_script()
        self.assertIsInstance(ref, dict, "Raspunsul de la script ar trebui sa fie un dictionar")
        self.assertIsInstance(ref['temp'], float, "Raspunsul de la script ar trebui sa fie un float pentru temperatura")
        self.assertIsInstance(ref['hum'], float, "Raspunsul de la script ar trebui sa fie un float pentru umiditate")
        self.assertIsInstance(ref['press'], float, "Raspunsul de la script ar trebui sa fie un float pentru presiune")
        



if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(f'{script_dir}\\testing', 'raspi_connect.txt')
    with open(file_path, 'w') as f:
        f.write(f"Test pornit la date de: {datetime.now().strftime("%d/%m/%Y")} ora: {datetime.now().strftime("%H:%M:%S")}\n")
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.TextTestRunner.run = runner.run
        unittest.main(exit=False)