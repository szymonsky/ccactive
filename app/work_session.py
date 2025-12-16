# loguje lub wylogowuje użytkownika i zapisuje sesję w tabeli work_sessions
# dodatkowo zapisuje aktualnie zalogowanego użytkownika do pliku current_user.txt,
# który służy do identyfikacji aktywnej sesji w innych skryptach

import os
import sys

# dodanie ścieżki do katalogu app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

connection = get_connection()

with connection.cursor() as cursor:
    # pobierz listę użytkowników
    cursor.execute("SELECT user_id, username FROM users ORDER BY user_id")
    users = cursor.fetchall()

    print("dostępni użytkownicy:")
    for u in users:
        print(f"{u[0]}: {u[1]}")

    try:
        user_id = int(input("\npodaj ID użytkownika do zalogowania/wylogowania: "))
    except ValueError:
        print("błąd: podano niepoprawny numer.")
        exit()

    # sprawdź czy jest aktywna sesja
    cursor.execute("""
        SELECT session_id FROM work_sessions
        WHERE user_id = :user_id AND logout_time IS NULL
    """, {"user_id": user_id})
    session = cursor.fetchone()

    if session:
        # wylogowanie
        cursor.execute("""
            UPDATE work_sessions
            SET logout_time = CURRENT_TIMESTAMP
            WHERE session_id = :session_id
        """, {"session_id": session[0]})

        # usuń plik current_user.txt
        if os.path.exists("current_user.txt"):
            os.remove("current_user.txt")

        print("\nużytkownik został wylogowany.")
    else:
        # logowanie
        cursor.execute("""
            INSERT INTO work_sessions (user_id) VALUES (:user_id)
        """, {"user_id": user_id})

        # zapisz ID użytkownika do pliku
        with open("current_user.txt", "w", encoding="utf-8") as f:
            f.write(str(user_id))

        print("\nużytkownik został zalogowany.")

    connection.commit()

connection.close()
