from dotenv import load_dotenv
from all_sensors.read_data import read_temp, read_pressure, read_hum
import time
from datetime import datetime
import os
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


load_dotenv()

CREDENTIALS: str = os.getenv("CREDENTIALS")
END_POINT: str = os.getenv("END_POINT")
URL_ADR: str = os.getenv("URL_DATA")

cred = credentials.Certificate(CREDENTIALS)
firebase_admin.initialize_app(cred, {
    "databaseURL": URL_ADR
})

while True:
    try:
        ref = db.reference(f"/status/{END_POINT}")
    except Exception as e:
        time.sleep(3)
        continue
    
    else:
        temp: float = read_temp()
        press: float = read_pressure()
        hum: float = read_hum()
        ref.child("temp").push({"value_temp": temp, "day": datetime.now().strftime("%d-%m-%Y"), "hour": int(datetime.now().strftime("%H"))})
        ref.child("press").push({"value_press": press, "day": datetime.now().strftime("%d-%m-%Y"), "hour": int(datetime.now().strftime("%H"))})
        ref.child("hum").push({"value_hum": hum, "day": datetime.now().strftime("%d-%m-%Y"), "hour": int(datetime.now().strftime("%H"))})
        time.sleep(3600)
            