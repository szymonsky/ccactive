# dev-only: walidacja spójności danych testowych
#  sprawdza poprawność danych w tabelach status_logs i work_sessions na podstawie 3 reguł

import os
import sys
from datetime import datetime

# dodanie ścieżki do katalogu głównego, aby import z app.* działał poprawnie
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

# połączenie z bazą danych
connection = get_connection()
cursor = connection.cursor()

print("\n=== WALIDACJA DANYCH ===\n")

# reguła 1 – niezamknięte statusy starsze niż 1 dzień
print("1. niezamknięte statusy starsze niż 1 dzień:")
query1 = """
SELECT u.username, s.status_name, sl.timestamp_start
FROM status_logs sl
JOIN users u ON sl.user_id = u.user_id
JOIN statuses s ON sl.status_id = s.status_id
WHERE sl.timestamp_end IS NULL AND sl.timestamp_start < (SYSTIMESTAMP - INTERVAL '1' DAY)
"""
cursor.execute(query1)
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"[!] użytkownik: {row[0]} | status: {row[1]} | start: {row[2]}")
else:
    print("✓ brak problemów")

# reguła 2 – nakładające się statusy
print("\n2. nakładające się statusy:")
query2 = """
SELECT u.username, s1.timestamp_start, s1.timestamp_end, s2.timestamp_start, s2.timestamp_end
FROM status_logs s1
JOIN status_logs s2 ON s1.user_id = s2.user_id AND s1.log_id < s2.log_id
JOIN users u ON s1.user_id = u.user_id
WHERE s1.timestamp_end IS NOT NULL AND s2.timestamp_start < s1.timestamp_end AND s2.timestamp_end > s1.timestamp_start
"""
cursor.execute(query2)
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"[!] {row[0]} | s1: {row[1]} – {row[2]} vs s2: {row[3]} – {row[4]}")
else:
    print("✓ brak problemów")

# reguła 3 – status poza czasem aktywnej sesji
print("\n3. status przypisany poza czasem zalogowania użytkownika:")
query3 = """
SELECT u.username, s.status_name, sl.timestamp_start, sl.timestamp_end
FROM status_logs sl
JOIN users u ON sl.user_id = u.user_id
JOIN statuses s ON sl.status_id = s.status_id
WHERE NOT EXISTS (
    SELECT 1 FROM work_sessions ws
    WHERE ws.user_id = sl.user_id
    AND sl.timestamp_start >= ws.login_time
    AND (sl.timestamp_end <= ws.logout_time OR ws.logout_time IS NULL)
)
"""
cursor.execute(query3)
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"[!] {row[0]} | status: {row[1]} | {row[2]} – {row[3]}")
else:
    print("✓ brak problemów")

# zakończenie
cursor.close()
connection.close()
print("\n=== KONIEC WALIDACJI ===\n")
