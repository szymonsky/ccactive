# to testowe połączenie z bazą danych z jawnie wpisanymi danymi logowania
# używać tylko lokalnie lub przy szybkim testowaniu połączenia


import sys
import os

# dodaj ścieżkę do katalogu głównego projektu, aby można było zaimportować moduły z app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

# połączenie z bazą danych
connection = get_connection()

# kursor i zapytanie
with connection.cursor() as cursor:
    cursor.execute("SELECT username, role_name, status_name, timestamp_start FROM view_current_status")
    rows = cursor.fetchall()

    print("aktualny status agentów:\n")
    for row in rows:
        print(f"użytkownik: {row[0]} | rola: {row[1]} | status: {row[2]} | start: {row[3]}")

# zamknięcie połączenia
connection.close()
