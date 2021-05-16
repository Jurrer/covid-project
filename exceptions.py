class ZlyFormatPliku(Exception):
    def __init__(self):
        msg = "Błąd! Oczekiwałem pliku .csv!"
        super().__init__(msg)

class ZleDane(Exception):
    def __init__(self):
        msg = "Błąd! Plik zawiera nieprawidłowe dane!"
        super().__init__(msg)