import smbus2

bus = smbus2.SMBus(1)
address = 0x77  # Sau 0x77, dacă e cazul

try:
    chip_id = bus.read_byte_data(address, 0xD0)  # Registrul ID pentru BME680
    print(f"Senzor detectat! ID: {chip_id}")
except Exception as e:
    print(f"Eroare la citirea senzorului: {e}")
