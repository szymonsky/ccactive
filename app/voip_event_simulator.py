# symulator zdarzeń voip: generuje zdarzenia typu call_started / call_ended
# w ramach Mminimum viable product zastępuje realną integrację z linphone/asterisk

import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.status_service import change_status
from app.db_connection import get_connection


def _read_logged_user_id() -> int | None:
    # odczytuje user_id z current_user.txt
    user_file = "current_user.txt"
    if not os.path.exists(user_file):
        return None

    with open(user_file, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    if not raw.isdigit():
        return None

    return int(raw)


def _get_status_id_by_name(status_name: str) -> int:
    # pobiera status_id dla podanej nazwy statusu
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status_id
        FROM statuses
        WHERE LOWER(status_name) = LOWER(:name)
    """, {"name": status_name})
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:
        raise ValueError(f"nie znaleziono statusu w bazie: {status_name}")

    return int(row[0])


def main():
    # mapowanie zdarzeń voip -> statusy w systemie
    # możesz zmienić nazwy statusów, jeśli w bazie są inne
    status_call = _get_status_id_by_name("Rozmowa")
    status_available = _get_status_id_by_name("Dostępny")

    user_id = _read_logged_user_id()
    if user_id is None:
        print("\nbrak zalogowanego użytkownika (current_user.txt).")
        print("najpierw uruchom work_session.py i zaloguj agenta.")
        return

    # proste menu zdarzeń
    print("\n--- voip event simulator ---")
    print(f"zalogowany user_id: {user_id}")
    print("1. call_started (ustaw status: Rozmowa)")
    print("2. call_ended (ustaw status: Dostępny)")
    print("0. wyjście")

    choice = input("\nwybierz zdarzenie: ").strip()

    if choice == "0":
        return

    # generujemy przykładowe external_call_id (jakby pochodziło z systemu voip)
    call_id = str(uuid.uuid4())

    if choice == "1":
        change_status(
            user_id=user_id,
            status_id=status_call,
            source="voip",
            external_call_id=call_id
        )
        print(f"\nzdarzenie call_started zapisane (external_call_id={call_id})")

    elif choice == "2":
        change_status(
            user_id=user_id,
            status_id=status_available,
            source="voip",
            external_call_id=call_id
        )
        print(f"\nzdarzenie call_ended zapisane (external_call_id={call_id})")

    else:
        print("\nniepoprawny wybór.")


if __name__ == "__main__":
    main()
