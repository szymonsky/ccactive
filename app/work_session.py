# obsługuje logowanie i wylogowanie agenta, zapisując sesje w work_sessions
import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime

# wczytaj dane z pliku .env
load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

connection = oracledb.connect(user=username, password=password, dsn=dsn)

with connection.cursor() as cursor:
    # lista użytkowników
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    print("dostępni użytkownicy:")
    for user in users:
        print(f"{user[0]}: {user[1]}")

    user_id = int(input("\npodaj ID użytkownika do zalogowania/wylogowania: "))

    # sprawdź czy użytkownik ma aktywną sesję (logout_time IS NULL)
    cursor.execute("""
        SELECT session_id FROM work_sessions
        WHERE user_id = :1 AND logout_time IS NULL
        ORDER BY login_time DESC FETCH FIRST 1 ROWS ONLY
    """, (user_id,))

    row = cursor.fetchone()

    if row:
        # jeśli jest aktywna sesja – wyloguj
        session_id = row[0]
        cursor.execute("""
            UPDATE work_sessions
            SET logout_time = :1
            WHERE session_id = :2
        """, (datetime.now(), session_id))
        print("\nużytkownik został wylogowany.")
    else:
        # jeśli nie ma aktywnej sesji – zaloguj
        cursor.execute("""
            INSERT INTO work_sessions (user_id, login_time)
            VALUES (:1, :2)
        """, (user_id, datetime.now()))
        print("\nużytkownik został zalogowany.")

    connection.commit()

connection.close()