# główne GUI aplikacji CCActive – zmiana statusu użytkownika

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# dodanie ścieżki głównej do importu app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import funkcji pomocniczych i połączenia z bazą
from app.utils import get_users, get_statuses
from app.db_connection import get_connection

class CCActiveGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CCActive GUI")
        self.geometry("400x300")
        self.resizable(False, False)

        # tworzy elementy interfejsu
        self.create_widgets()

    def create_widgets(self):
        # rozwijana lista użytkowników
        ttk.Label(self, text="Wybierz użytkownika:").pack(pady=10)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(self, textvariable=self.user_var, state="readonly")
        self.user_combo['values'] = [f"{user[0]}: {user[1]}" for user in get_users()]
        self.user_combo.pack()

        # rozwijana lista statusów
        ttk.Label(self, text="Wybierz nowy status:").pack(pady=10)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(self, textvariable=self.status_var, state="readonly")
        self.status_combo['values'] = [f"{status[0]}: {status[1]}" for status in get_statuses()]
        self.status_combo.pack()

        # przycisk do zatwierdzenia zmiany
        ttk.Button(self, text="Zmień status", command=self.change_status).pack(pady=20)

    def change_status(self):
        # sprawdzenie czy wybrano użytkownika i status
        user_entry = self.user_var.get()
        status_entry = self.status_var.get()

        if not user_entry or not status_entry:
            messagebox.showwarning("Błąd", "Wybierz użytkownika i status.")
            return

        # wyciągnięcie ID z wpisów
        user_id = int(user_entry.split(":")[0])
        status_id = int(status_entry.split(":")[0])

        # wykonanie zmiany statusu w bazie
        connection = get_connection()
        cursor = connection.cursor()

        # zakończenie poprzedniego statusu (jeśli istnieje)
        cursor.execute("""
            UPDATE status_logs
            SET timestamp_end = SYSTIMESTAMP
            WHERE user_id = :user_id AND timestamp_end IS NULL
        """, {"user_id": user_id})

        # dodanie nowego statusu
        cursor.execute("""
            INSERT INTO status_logs (user_id, status_id)
            VALUES (:user_id, :status_id)
        """, {"user_id": user_id, "status_id": status_id})

        connection.commit()
        cursor.close()
        connection.close()

        # komunikat o sukcesie
        messagebox.showinfo("Sukces", "Status został zmieniony.")

# uruchomienie GUI
if __name__ == "__main__":
    app = CCActiveGUI()
    app.mainloop()
