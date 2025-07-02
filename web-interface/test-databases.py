import unittest
from datetime import datetime
import os


class TestFoundIP(unittest.TestCase):
    def test_connect(self):
        from databases.db_access import DbAccess
        found_ip = DbAccess()
        ref = found_ip.connect()
        self.assertIsNotNone(ref, "Conexiunea la Firebase ar trebui sa fie stabilita")

    def test_get_ip(self):
        from databases.db_access import DbAccess
        found_ip = DbAccess()
        ip = found_ip.get_ip()
        self.assertIsInstance(ip, str, "IP address ar trebui sa fie un string")

    def test_get_ssid(self):
        from databases.db_access import DbAccess
        found_ip = DbAccess()
        ssid = found_ip.get_ssid()
        self.assertIsInstance(ssid, str, "SSID ar trebuie sa fie un string")
    def test_get_data(self):
        from databases.db_access import DbAccess
        found_ip = DbAccess()
        data = found_ip.get_data()
        self.assertIsInstance(data, dict, "Datele obtinute ar trebui sa fie un dictionar")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(f'{script_dir}\\testing', 'test_databases.txt')
    with open(file_path, 'w') as f:
        f.write(f"Test pornit la date de: {datetime.now().strftime("%d/%m/%Y")} ora: {datetime.now().strftime("%H:%M:%S")}\n")
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.TextTestRunner.run = runner.run
        unittest.main(exit=False)