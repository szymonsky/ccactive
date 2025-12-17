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