# gui administracyjne (read-only)
# panel monitorujący pracę call center
#
# funkcjonalności:
# - podgląd aktualnych statusów agentów
# - dashboard liczbowy (liczba agentów w statusach)
# - dashboard czasowy (czas pracy agentów w statusach – bieżący dzień)
# - eksport raportu historycznego do pliku csv

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

# dodanie ścieżki do katalogu głównego projektu
# umożliwia poprawne importy modułów aplikacji
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_connection import get_connection


class GUIAdmin(tk.Tk):
    """
    główne okno panelu administracyjnego ccactive

    gui ma charakter wyłącznie odczytowy (read-only)
    wszystkie dane pobierane są bezpośrednio z bazy danych
    """

    def __init__(self):
        super().__init__()

        # konfiguracja podstawowych parametrów okna
        self.title("CCActive – panel administracyjny")
        self.geometry("950x650")
        self.resizable(False, False)

        # inicjalizacja komponentów gui
        self.create_widgets()

        # wczytanie danych początkowych
        self.refresh_all()

    # ==========================================================
    # SEKCJA: BUDOWA INTERFEJSU UŻYTKOWNIKA
    # ==========================================================

    def create_widgets(self):
        """
        tworzy wszystkie elementy interfejsu użytkownika
        (tabele, dashboardy, przyciski)
        """

        # --- sekcja 1: aktualne statusy agentów ---
        ttk.Label(
            self,
            text="Aktualne statusy agentów",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(10, 5))

        # tabela prezentująca bieżący status każdego agenta
        columns = ("username", "role", "status", "since")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=7
        )

        self.tree.heading("username", text="Agent")
        self.tree.heading("role", text="Rola")
        self.tree.heading("status", text="Status")
        self.tree.heading("since", text="Od")

        self.tree.column("username", width=160)
        self.tree.column("role", width=100)
        self.tree.column("status", width=160)
        self.tree.column("since", width=180)

        self.tree.pack(fill=tk.X, padx=10)

        # --- sekcja 2: dashboard liczbowy ---
        ttk.Label(
            self,
            text="Statusy bieżące – liczba agentów",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(15, 5))

        # kontener na dynamicznie generowane etykiety statusów
        self.dashboard_count_frame = ttk.Frame(self)
        self.dashboard_count_frame.pack(pady=5)

        # --- sekcja 3: dashboard czasowy ---
        ttk.Label(
            self,
            text="Czas pracy agentów w statusach – bieżący dzień (minuty)",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(20, 5))

        # tabela prezentująca czas pracy agentów w statusach
        time_columns = ("username", "status", "minutes")

        self.time_tree = ttk.Treeview(
            self,
            columns=time_columns,
            show="headings",
            height=8
        )

        self.time_tree.heading("username", text="Agent")
        self.time_tree.heading("status", text="Status")
        self.time_tree.heading("minutes", text="Minuty (dzisiaj)")

        self.time_tree.column("username", width=160)
        self.time_tree.column("status", width=160)
        self.time_tree.column("minutes", width=140, anchor="center")

        self.time_tree.pack(fill=tk.X, padx=10)

        # --- sekcja 4: przyciski sterujące ---
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=20)

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

    # ==========================================================
    # SEKCJA: WCZYTYWANIE DANYCH Z BAZY
    # ==========================================================

    def load_current_statuses(self):
        """
        wczytuje aktualne statusy agentów
        dane pobierane są z widoku view_current_status
        """

        # wyczyszczenie tabeli
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

        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

        cursor.close()
        connection.close()

    def load_dashboard_status_count(self):
        """
        dashboard liczbowy:
        liczba agentów w poszczególnych statusach (stan bieżący)
        """

        # usunięcie poprzednich etykiet
        for widget in self.dashboard_count_frame.winfo_children():
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

        col = 0
        for status_name, count in cursor.fetchall():
            ttk.Label(
                self.dashboard_count_frame,
                text=f"{status_name}: {count}",
                font=("Segoe UI", 10)
            ).grid(row=0, column=col, padx=15)
            col += 1

        cursor.close()
        connection.close()

    def load_dashboard_time_today(self):
        """
        dashboard czasowy:
        dzienny czas pracy agentów w statusach
        dane pobierane są z widoku view_today_agent_status_time
        """

        # wyczyszczenie tabeli dashboardu czasowego
        for row in self.time_tree.get_children():
            self.time_tree.delete(row)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                username,
                status_name,
                minutes_today
            FROM view_today_agent_status_time
            ORDER BY username, status_name
        """)

        for row in cursor.fetchall():
            self.time_tree.insert("", tk.END, values=row)

        cursor.close()
        connection.close()

    # ==========================================================
    # SEKCJA: OPERACJE UŻYTKOWNIKA
    # ==========================================================

    def refresh_all(self):
        """
        odświeża wszystkie sekcje panelu administracyjnego
        """

        self.load_current_statuses()
        self.load_dashboard_status_count()
        self.load_dashboard_time_today()

    def export_csv(self):
        """
        uruchamia moduł eksportu raportu historycznego do pliku csv
        """

        try:
            subprocess.run(
                [sys.executable, "app/export_report_csv.py"],
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
