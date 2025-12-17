# dev-only: raport zbiorczy w trybie cli
# wykorzystywany do testów i walidacji danych
# łączy się z bazą i wyświetla raport czasu pracy agentów w podziale na dni i statusy
import os
import sys

# dodanie ścieżki do katalogu głównego projektu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

# ścieżka do pliku sql z zapytaniem
sql_file_path = os.path.join("sql", "select_status_time_report.sql")

# wczytaj zapytanie z pliku
with open(sql_file_path, "r", encoding="utf-8") as file:
    query = file.read()

# połączenie z bazą danych
connection = get_connection()

with connection.cursor() as cursor:
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nRaport czasu pracy agentów:\n")
    print("Użytkownik     | Status        | Dzień       | Minuty")
    print("-------------------------------------------------------")
    for row in rows:
        print(f"{row[0]:13} | {row[1]:13} | {row[2].date()} | {int(row[3])}")

connection.close()
