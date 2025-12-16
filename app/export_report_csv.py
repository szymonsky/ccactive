# eksportuje raport czasu pracy agentów do pliku CSV

import sys
import os
import csv
from datetime import datetime

# dodaje katalog główny projektu do ścieżki, żeby działał import z app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

# ustalenie katalogu głównego projektu
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# ustalenie daty dla nazwy pliku
today = datetime.today().strftime("%Y-%m-%d")
filename = f"report_{today}.csv"

# wczytaj zapytanie z pliku .sql
sql_path = os.path.join(BASE_DIR, 'sql', 'select_status_time_report.sql')
with open(sql_path, encoding="utf-8") as f:
    query = f.read()

# połączenie z bazą danych
connection = get_connection()

# wykonanie zapytania i zapis do pliku CSV
with connection.cursor() as cursor:
    cursor.execute(query)
    rows = cursor.fetchall()

    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Użytkownik", "Status", "Dzień", "Minuty"])
        writer.writerows(rows)

print(f"raport zapisany do pliku {filename}")

connection.close()