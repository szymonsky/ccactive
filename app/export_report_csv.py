# eksportuje raport czasu pracy agentów do pliku CSV
import csv
import os
from datetime import datetime
from db_connection import get_connection

# ustalenie daty dla nazwy pliku
today = datetime.today().strftime("%Y-%m-%d")
filename = f"report_{today}.csv"

# wczytaj zapytanie z pliku .sql
with open(os.path.join("sql", "select_status_time_report.sql"), encoding="utf-8") as f:
    query = f.read()

# połączenie z bazą
connection = get_connection()

with connection.cursor() as cursor:
    cursor.execute(query)
    rows = cursor.fetchall()

# ścieżka docelowa
output_path = os.path.join(os.getcwd(), filename)

# zapis do pliku CSV
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Użytkownik', 'Status', 'Dzień', 'Minuty'])
    writer.writerows(rows)

print(f"raport zapisany do pliku: {output_path}")
connection.close()
