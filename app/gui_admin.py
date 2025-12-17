# gui administracyjne (read-only)
# podgląd aktualnych statusów agentów + prosty dashboard + eksport csv

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

# dodaj ścieżkę do katalogu głównego projektu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection


class GUIAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CCActive – panel administracyjny")
        self.geometry("800x450")
        self.resizable(False, False)

        self.create_widgets()
        self.load_data()
        self.load_dashboard()

    def create_widgets(self):
        # --- tytuł tabeli ---
        ttk.Label(
            self,
            text="Aktualne statusy agentów",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(10, 5))

        # --- tabela statusów ---
        columns = ("username", "role", "status", "since")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self.tree.heading("username", text="Użytkownik")
        self.tree.heading("role", text="Rola")
        self.tree.heading("status", text="Status")
        self.tree.heading("since", text="Od")

        self.tree.column("username", width=160)
        self.tree.column("role", width=100)
        self.tree.column("status", width=160)
        self.tree.column("since", width=180)

        self.tree.pack(fill=tk.X, padx=10)

        # --- dashboard ---
        ttk.Label(
            self,
            text="Statusy bieżące (liczba agentów)",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(15, 5))

        self.dashboard_frame = ttk.Frame(self)
        self.dashboard_frame.pack(pady=5)

        self.dashboard_labels = {}

        # --- przyciski ---
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=15)

        ttk.Button(
            buttons_frame,
            text="Odśwież dane",
            command=self.refresh_all
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            buttons_frame,
            text="Eksportuj raport CSV",
            command=self.export_csv
        ).grid(row=0, column=1, padx=10)

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

    def load_dashboard(self):
        # dashboard admina: zliczenie liczby agentów w poszczególnych statusach (stan bieżący)

        # usuń stare etykiety
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                status_name,
                COUNT(*) AS agent_count
            FROM view_current_status
            GROUP BY status_name
            ORDER BY status_name
        """)

        rows = cursor.fetchall()

        col = 0
        for status_name, count in rows:
            label = ttk.Label(
                self.dashboard_frame,
                text=f"{status_name}: {count}",
                font=("Segoe UI", 10)
            )
            label.grid(row=0, column=col, padx=15)
            col += 1

        cursor.close()
        connection.close()

    def refresh_all(self):
        self.load_data()
        self.load_dashboard()

    def export_csv(self):
        try:
            subprocess.run(
                ["python", "app/export_report_csv.py"],
                check=True
            )
            messagebox.showinfo(
                "Eksport zakończony",
                "Raport CSV został wygenerowany poprawnie."
            )
        except Exception as e:
            messagebox.showerror(
                "Błąd eksportu",
                f"Nie udało się wygenerować raportu CSV:\n{e}"
            )


if __name__ == "__main__":
    app = GUIAdmin()
    app.mainloop()
