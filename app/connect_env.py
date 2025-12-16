# testowy skrypt do ręcznego ustawiania statusu agenta – wykorzystuje get_connection() z app.db_connection

import os
import sys
from datetime import datetime

# dodanie ścieżki do katalogu głównego
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

# połączenie z bazą danych
connection = get_connection()

with connection.cursor() as cursor:
    # pobierz użytkowników
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    print("dostępni użytkownicy:")
    for user in users:
        print(f"{user[0]}: {user[1]}")

    user_id = int(input("\npodaj ID użytkownika: "))

    # pobierz statusy
    cursor.execute("SELECT status_id, status_name FROM statuses")
    statuses = cursor.fetchall()

    print("\ndostępne statusy:")
    for status in statuses:
        print(f"{status[0]}: {status[1]}")

    status_id = int(input("\npodaj ID statusu: "))

    # dodaj nowy wpis do status_logs
    cursor.execute("""
        INSERT INTO status_logs (user_id, status_id, timestamp_start)
        VALUES (:1, :2, :3)
    """, (user_id, status_id, datetime.now()))

    connection.commit()
    print("\nstatus został zmieniony.")

connection.close()
