from all_sensors.read_data import read_temp, read_pressure, read_hum
from datetime import datetime

temp: float = read_temp()
press: float = read_pressure()
hum: float = read_hum()


all_data: dict = {
      "hour" : datetime.now().strftime("%H:%M:%S"),
      "temp": temp,
      "press": press,
      "hum": hum
    }


print(all_data)