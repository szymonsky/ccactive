# zawiera funkcję get_connection() do połączenia z bazą danych Oracle
import os
import oracledb
from dotenv import load_dotenv

# wczytaj dane z pliku .env (plik znajduje się w katalogu app)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def get_connection():
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    if not all([username, password, dsn]):
        raise ValueError("brakuje danych połączeniowych w pliku .env")

    return oracledb.connect(user=username, password=password, dsn=dsn)
