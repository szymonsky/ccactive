# to graficzny interfejs do zmiany statusu użytkownika w aplikacji CCActive

import tkinter as tk
print("==== STARTUJĘ GUI CCActive ====")
from tkinter import ttk, messagebox
import os
import sys

# dodaj ścieżkę do katalogu głównego, by importy z app działały
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import get_users, get_statuses
from app.db_connection import get_connection

class CCActiveGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CCActive – zmiana statusu agenta")
        self.geometry("400x300")
        self.resizable(False, False)

        self.create_widgets()  #  to wywołuje wszystkie elementy GUI

    def create_widgets(self):
        ttk.Label(self, text="Wybierz użytkownika:").pack(pady=5)
        self.user_combo = ttk.Combobox(self, state="readonly")
        self.user_combo['values'] = [f"{user[0]}: {user[1]}" for user in get_users()]
        self.user_combo.pack()

        ttk.Label(self, text="Wybierz nowy status:").pack(pady=5)
        self.status_combo = ttk.Combobox(self, state="readonly")
        self.status_combo['values'] = [f"{status[0]}: {status[1]}" for status in get_statuses()]
        self.status_combo.pack()

        ttk.Button(self, text="Zmień status", command=self.change_status).pack(pady=20)

    def change_status(self):
        user = self.user_combo.get()
        status = self.status_combo.get()

        if not user or not status:
            messagebox.showwarning("Błąd", "Wybierz użytkownika i status.")
            return

        user_id = int(user.split(":")[0])
        status_id = int(status.split(":")[0])

        connection = get_connection()
        cursor = connection.cursor()

        # zakończ poprzedni status (jeśli jest otwarty)
        cursor.execute("""
            UPDATE status_logs
            SET timestamp_end = SYSTIMESTAMP
            WHERE user_id = :uid AND timestamp_end IS NULL
        """, [user_id])

        # dodaj nowy status
        cursor.execute("""
            INSERT INTO status_logs (user_id, status_id, timestamp_start)
            VALUES (:uid, :sid, SYSTIMESTAMP)
        """, [user_id, status_id])

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Sukces", "Status został zmieniony.")

if __name__ == "__main__":
    app = CCActiveGUI()
    app.mainloop()