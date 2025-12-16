# generuje testowe wpisy statusów do tabeli status_logs dla wybranych użytkowników
import oracledb
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# wczytaj dane z pliku .env --plik .env nie jest w katalogu glownym
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'app', '.env'))

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

# konfiguracja generatora
DAYS_BACK = 3  # liczba dni wstecz do generowania logów
ENTRIES_PER_USER = 5  # ile wpisów statusów na użytkownika
STATUS_IDS = [1, 2, 3, 4]  # id statusów: Dostępny, Rozmowa, Przerwa, Offline

# połączenie z bazą danych
connection = oracledb.connect(user=username, password=password, dsn=dsn)

with connection.cursor() as cursor:
    # pobierz użytkowników
    cursor.execute("SELECT user_id FROM users ORDER BY user_id")
    users = [row[0] for row in cursor.fetchall()]

    for user_id in users:
        print(f"generuję dane testowe dla użytkownika ID {user_id}...")

        for _ in range(ENTRIES_PER_USER):
            # losowy dzień z ostatnich DAYS_BACK dni
            days_ago = random.randint(0, DAYS_BACK - 1)
            base_date = datetime.now() - timedelta(days=days_ago)

            # losowa godzina startu i długość statusu (5–120 min)
            hour = random.randint(7, 17)
            minute = random.randint(0, 59)
            duration = random.randint(5, 120)

            start_time = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=duration)

            status_id = random.choice(STATUS_IDS)

            cursor.execute("""
                INSERT INTO status_logs (user_id, status_id, timestamp_start, timestamp_end, source)
                VALUES (:user_id, :status_id, :start_time, :end_time, 'generator')
            """, {
                "user_id": user_id,
                "status_id": status_id,
                "start_time": start_time,
                "end_time": end_time
            })

    connection.commit()
    print("\nzakończono generowanie wpisów testowych.")

connection.close()
