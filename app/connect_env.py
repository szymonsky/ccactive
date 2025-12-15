#  skrypt pozwala ręcznie zmienić status agenta, dodając nowy wpis do status_logs
import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime

# wczytaj dane z pliku .env
load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

# połączenie z bazą danych
connection = oracledb.connect(user=username, password=password, dsn=dsn)

with connection.cursor() as cursor:
    # pobierz dostępnych użytkowników
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    print("dostępni użytkownicy:")
    for user in users:
        print(f"{user[0]}: {user[1]}")

    user_id = int(input("\npodaj ID użytkownika: "))

    # pobierz dostępne statusy
    cursor.execute("SELECT status_id, status_name FROM statuses")
    statuses = cursor.fetchall()

    print("\ndostępne statusy:")
    for status in statuses:
        print(f"{status[0]}: {status[1]}")

    status_id = int(input("\npodaj ID statusu: "))

    # wstaw nowy wpis do status_logs
    cursor.execute("""
        INSERT INTO status_logs (user_id, status_id, timestamp_start)
        VALUES (:1, :2, :3)
    """, (user_id, status_id, datetime.now()))

    connection.commit()
    print("\nstatus został zmieniony.")

connection.close()
