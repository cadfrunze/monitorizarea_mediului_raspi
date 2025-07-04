from model.all_data import AllData
import unittest
from datetime import datetime
import os

class TestAllData(unittest.TestCase):
    def setUp(self):
        self.all_data = AllData()

    def test_data_range(self):
        start_hour = 0
        end_hour = 23
        ziua1 = "03-06-2025"
        ziua2 = "05-06-2025"
        
        result = self.all_data.data_range(start_hour, end_hour, ziua1, ziua2)
        
        self.assertIsInstance(result, dict, "Rezultatul ar trebui sa fie un dictionar")
        self.assertIn("temp", result, "Dictionarul ar trebui sa contina cheia 'temp'")
        self.assertIn("hum", result, "Dictionarul ar trebui sa contina cheia 'hum'")
        self.assertIn("press", result, "Dictionarul ar trebui sa contina cheia 'press'")
        self.assertGreater(len(result["temp"]), 0, "Lista de date pentru temperatura ar trebui sa contina date")


if __name__ == '__main__':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(f'{script_dir}\\testing', 'all_data.txt')
        with open(file_path, 'w') as f:
            f.write(f"Test pornit la date de: {datetime.now().strftime("%d/%m/%Y")} ora: {datetime.now().strftime("%H:%M:%S")}\n")
            runner = unittest.TextTestRunner(stream=f, verbosity=2)
            unittest.TextTestRunner.run = runner.run
            unittest.main(exit=False)