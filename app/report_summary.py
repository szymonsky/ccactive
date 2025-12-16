# łączy się z bazą i wyświetla raport czasu pracy agentów w podziale na dni i statusy
import oracledb
import os
from dotenv import load_dotenv

# wczytaj dane z pliku .env
load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

# ścieżka do pliku sql z zapytaniem
sql_file_path = "../sql/select_status_time_report.sql"

# wczytaj zapytanie z pliku
with open(sql_file_path, "r", encoding="utf-8") as file:
    query = file.read()

# połączenie z bazą danych
connection = oracledb.connect(user=username, password=password, dsn=dsn)

with connection.cursor() as cursor:
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nRaport czasu pracy agentów:\n")
    print("Użytkownik     | Status        | Dzień       | Minuty")
    print("-------------------------------------------------------")
    for row in rows:
        print(f"{row[0]:13} | {row[1]:13} | {row[2].date()} | {int(row[3])}")

connection.close()
