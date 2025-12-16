# funkcje pomocnicze do pobierania użytkowników i statusów z bazy
import os
import sys

# dodaj katalog główny do ścieżki, aby import z app.* działał poprawnie
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection

def get_users():
    # zwraca listę wszystkich użytkowników (id + nazwa)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, username FROM users ORDER BY user_id")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_statuses():
    # zwraca listę wszystkich statusów (id + nazwa)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT status_id, status_name FROM statuses ORDER BY status_id")
    statuses = cursor.fetchall()
    cursor.close()
    connection.close()
    return statuses