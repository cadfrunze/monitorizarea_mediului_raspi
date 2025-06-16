import datetime
import os
from data import cred_brut, url_adrr, end_point
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


ip_local = os.popen("hostname -I").read().strip()

#print(f"Adresa IP local?: {ip_local}")

ssid = os.popen("iwgetid -r").read().strip()
#print(f"SSID-ul routerului: {ssid}")

cred = credentials.Certificate(cred_brut)
firebase_admin.initialize_app(cred, {
    "databaseURL": url_adrr
})
try:
    ref = db.reference(f"/status/{end_point}")
    ref.set({
        "adresa": f"{ip_local}",
        "data": f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}",
        "ora": f"{datetime.datetime.now().strftime('%H:%M')}",
        "retea": f"{ssid}"
    })

except Exception as e:
    raise e
