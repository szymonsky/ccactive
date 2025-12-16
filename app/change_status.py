# cli agenta – ręczna zmiana statusu zalogowanego użytkownika

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.status_service import change_status
from app.db_connection import get_connection

# sprawdź czy istnieje plik current_user.txt
user_file = "current_user.txt"
if not os.path.exists(user_file):
    print("\nbrak zalogowanego użytkownika.")
    exit()

with open(user_file, "r", encoding="utf-8") as f:
    user_id = f.read().strip()

if not user_id.isdigit():
    print("\nbłędne dane użytkownika.")
    exit()

user_id = int(user_id)

# pobierz statusy
connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT status_id, status_name FROM statuses ORDER BY status_id")
statuses = cursor.fetchall()

print("\ndostępne statusy:")
for status in statuses:
    print(f"{status[0]}: {status[1]}")

try:
    status_id = int(input("\npodaj ID nowego statusu: "))
except ValueError:
    print("błędny numer.")
    exit()

cursor.close()
connection.close()

# zmiana statusu przez wspólną logikę
change_status(
    user_id=user_id,
    status_id=status_id,
    source="manual"
)

print("\nstatus został zmieniony.")
