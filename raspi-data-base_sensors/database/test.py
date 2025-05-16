import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    print("Conectat la baza de date!")
    conn.close()
except mariadb.Error as e:
    print(f"Eroare la conectare: {e}")