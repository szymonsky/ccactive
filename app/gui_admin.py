# gui administracyjne (read-only)
# podgląd aktualnych statusów agentów

import tkinter as tk
from tkinter import ttk
import os
import sys

# dodaj ścieżkę do katalogu głównego projektu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection


class GUIAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CCActive – panel administracyjny")
        self.geometry("600x300")
        self.resizable(False, False)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # tabela statusów
        columns = ("username", "role", "status", "since")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("username", text="Użytkownik")
        self.tree.heading("role", text="Rola")
        self.tree.heading("status", text="Status")
        self.tree.heading("since", text="Od")

        self.tree.column("username", width=150)
        self.tree.column("role", width=100)
        self.tree.column("status", width=150)
        self.tree.column("since", width=180)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # przycisk odświeżania
        ttk.Button(self, text="Odśwież", command=self.load_data).pack(pady=5)

    def load_data(self):
        # wyczyść tabelę
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                username,
                role_name,
                status_name,
                timestamp_start
            FROM view_current_status
            ORDER BY username
        """)

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        cursor.close()
        connection.close()


if __name__ == "__main__":
    app = GUIAdmin()
    app.mainloop()
