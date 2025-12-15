import oracledb

# dane logowania
username = "ccactive_user"
password = "ccactive"  # <-- USTAWIĆ HASŁO - NIE UJAWNIAĆ!
dsn = "localhost/XEPDB1"

# połączenie
connection = oracledb.connect(user=username, password=password, dsn=dsn)

# kursor i zapytanie
with connection.cursor() as cursor:
    cursor.execute("SELECT username, role_name, status_name, timestamp_start FROM view_current_status")
    rows = cursor.fetchall()

    print("Aktualny status agentów:\n")
    for row in rows:
        print(f"Użytkownik: {row[0]} | Rola: {row[1]} | Status: {row[2]} | Start: {row[3]}")

# zamknięcie połączenia
connection.close()
