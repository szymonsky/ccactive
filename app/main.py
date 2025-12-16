# ten skrypt stanowi główny interfejs aplikacji tekstowej CCActive – pozwala na wybór akcji
import os
import report_summary
import work_session

# wersja rozwojowa – podstawowe menu tekstowe

def main_menu():
    while True:
        print("\n--- CCActive – menu główne ---")
        print("1. zaloguj / wyloguj użytkownika")
        print("2. pokaż raport czasu pracy")
        print("0. wyjście")

        choice = input("\nWybierz opcję: ")

        if choice == "1":
            os.system("python work_session.py")
        elif choice == "2":
            os.system("python report_summary.py")
        elif choice == "0":
            print("Zamykam aplikację.")
            break
        else:
            print("\nNiepoprawny wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main_menu()
