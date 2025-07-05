import unittest
from datetime import datetime
import os


class TestFoundIP(unittest.TestCase):
    """Testele pentru clasa IpRaspi care se ocupa cu conexiunea la baza de date Firebase"""
    def test_connect(self):
        """Testeaza conexiunea la baza de date Firebase"""
        from databases.found_ip import IpRaspi
        found_ip = IpRaspi()
        ref = found_ip.connect()
        self.assertIsNotNone(ref, "Conexiunea la Firebase ar trebui sa fie stabilita")

    def test_get_ip(self):
        """Testeaza obtinerea adresei IP din baza de date Firebase"""
        from databases.found_ip import IpRaspi
        found_ip = IpRaspi()
        ip = found_ip.get_ip()
        self.assertIsInstance(ip, str, "IP address ar trebui sa fie un string")

    def test_get_ssid(self):
        """Testeaza obtinerea SSID-ului din baza de date Firebase"""
        from databases.found_ip import IpRaspi
        found_ip = IpRaspi()
        ssid = found_ip.get_ssid()
        self.assertIsInstance(ssid, str, "SSID ar trebuie sa fie un string")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(f'{script_dir}\\testing', 'test_found_ip.txt')
    with open(file_path, 'w') as f:
        f.write(f"Test pornit la date de: {datetime.now().strftime("%d/%m/%Y")} ora: {datetime.now().strftime("%H:%M:%S")}\n")
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.TextTestRunner.run = runner.run
        unittest.main(exit=False)