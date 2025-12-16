# wspólna logika zmiany statusu użytkownika
# wykorzystywana przez cli agenta oraz symulator zdarzeń voip

from app.db_connection import get_connection
from datetime import datetime


def change_status(
    user_id: int,
    status_id: int,
    source: str = "manual",
    external_call_id: str | None = None
):
    # zmienia status użytkownika:
    # 1. zamyka poprzedni aktywny status
    # 2. dodaje nowy wpis do status_logs

    now = datetime.now()

    connection = get_connection()
    cursor = connection.cursor()

    # zamknięcie poprzedniego statusu (jeśli istnieje)
    cursor.execute("""
        UPDATE status_logs
        SET timestamp_end = :now
        WHERE user_id = :user_id
          AND timestamp_end IS NULL
    """, {
        "now": now,
        "user_id": user_id
    })

    # dodanie nowego statusu
    cursor.execute("""
        INSERT INTO status_logs (
            user_id,
            status_id,
            timestamp_start,
            source,
            external_call_id
        )
        VALUES (
            :user_id,
            :status_id,
            :now,
            :source,
            :external_call_id
        )
    """, {
        "user_id": user_id,
        "status_id": status_id,
        "now": now,
        "source": source,
        "external_call_id": external_call_id
    })

    connection.commit()
    cursor.close()
    connection.close()
