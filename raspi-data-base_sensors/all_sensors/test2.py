from read_data import read_temp, read_pressure, read_hum, read_gas
import time

while True:
  temp = read_temp()
  pressure = read_pressure()
  hum = read_hum()
  gas = read_gas()
  print(f"\n\ntemp: {temp}\npressure: {pressure}\nhumidity: {hum}\ngas: {gas}")
#  time.sleep(1)
