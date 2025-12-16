# testowa wersja zmiany statusu agenta z zamknięciem poprzedniego wpisu w status_logs
# używać tylko do testowania ręcznego lub debugowania

import os
import sys
from datetime import datetime

# dodanie ścieżki do katalogu głównego, aby import z app.* działał poprawnie
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

connection = get_connection()

with connection.cursor() as cursor:
    # pobierz użytkowników
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    print("dostępni użytkownicy:")
    for user in users:
        print(f"{user[0]}: {user[1]}")

    user_id = int(input("\npodaj ID użytkownika: "))

    # zamknij poprzedni status (ustaw timestamp_end)
    cursor.execute("""
        UPDATE status_logs
        SET timestamp_end = :1
        WHERE user_id = :2 AND timestamp_end IS NULL
    """, (datetime.now(), user_id))

    # pobierz statusy
    cursor.execute("SELECT status_id, status_name FROM statuses")
    statuses = cursor.fetchall()

    print("\ndostępne statusy:")
    for status in statuses:
        print(f"{status[0]}: {status[1]}")

    status_id = int(input("\npodaj ID nowego statusu: "))

    # dodaj nowy wpis
    cursor.execute("""
        INSERT INTO status_logs (user_id, status_id, timestamp_start)
        VALUES (:1, :2, :3)
    """, (user_id, status_id, datetime.now()))

    connection.commit()
    print("\nstatus został zmieniony.")

connection.close()
