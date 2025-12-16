# zmienia status zalogowanego użytkownika (na podstawie current_user.txt)
import oracledb
import os
from dotenv import load_dotenv

# wczytaj dane z .env
load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

# sprawdź czy istnieje plik current_user.txt
user_file = "current_user.txt"
if not os.path.exists(user_file):
    print("\nBrak zalogowanego użytkownika. Najpierw zaloguj się w opcji 1.")
    exit()

# odczytaj user_id z pliku
with open(user_file, "r", encoding="utf-8") as f:
    user_id = f.read().strip()

if not user_id.isdigit():
    print("\nNiepoprawne dane użytkownika w current_user.txt")
    exit()

# połączenie z bazą
connection = oracledb.connect(user=username, password=password, dsn=dsn)

with connection.cursor() as cursor:
    # pobierz listę dostępnych statusów
    cursor.execute("SELECT status_id, status_name FROM statuses ORDER BY status_id")
    statuses = cursor.fetchall()

    print("\nDostępne statusy:")
    for status in statuses:
        print(f"{status[0]}: {status[1]}")

    # wybór nowego statusu
    try:
        selected_status_id = int(input("\nPodaj ID nowego statusu: "))
    except ValueError:
        print("\nBłąd: podano niepoprawny numer.")
        exit()

    # zamknięcie poprzedniego aktywnego wpisu
    cursor.execute("""
        UPDATE status_logs
        SET timestamp_end = CURRENT_TIMESTAMP
        WHERE user_id = :user_id AND timestamp_end IS NULL
    """, {"user_id": user_id})

    # dodanie nowego wpisu
    cursor.execute("""
        INSERT INTO status_logs (user_id, status_id)
        VALUES (:user_id, :status_id)
    """, {"user_id": user_id, "status_id": selected_status_id})

    connection.commit()
    print("\nStatus został zmieniony.")

connection.close()
