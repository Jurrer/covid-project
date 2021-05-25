class ZlyFormatPliku(Exception):
    def __init__(self):
        msg = "Błąd! Oczekiwałem pliku .csv!"
        super().__init__(msg)


class ZleDane(Exception):
    def __init__(self):
        msg = "Błąd! Plik zawiera nieprawidłowe dane!"
        super().__init__(msg)


class LimitPanstw(Exception):
    def __init__(self):
        msg = "Błąd! Został osiągnięty limit państw (6)!"
        super().__init__(msg)


class BrakPliku(Exception):
    def __init__(self):
        msg = "Brak Pliku"
        super().__init__(msg)
