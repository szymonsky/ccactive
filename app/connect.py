import oracledb
import os
from dotenv import load_dotenv

# wczytaj dane z pliku .env
load_dotenv()

# dane logowania
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

# połączenie
connection = oracledb.connect(user=username, password=password, dsn=dsn)

# kursor i zapytanie
with connection.cursor() as cursor:
    cursor.execute("SELECT username, role_name, status_name, timestamp_start FROM view_current_status")
    rows = cursor.fetchall()

    print("Aktualny status agentów:\n")
    for row in rows:
        print(f"Użytkownik: {row[0]} | Rola: {row[1]} | Status: {row[2]} | Start: {row[3]}")

# zamknięcie połączenia
connection.close()
