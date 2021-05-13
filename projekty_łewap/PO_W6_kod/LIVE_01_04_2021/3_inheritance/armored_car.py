from car import Car


class ArmoredCar(Car):

    def __init__(self, mark, model, year_of_production, glass_thickness):
        super().__init__(mark, model, year_of_production)
        self.__glass_thickness = glass_thickness

    def create_secret_name(self):
        secret_name = f"{self._Car__mark}_{self._Car__model}_{self._Car__get_last_2_digits_of_year()}"
        return secret_name
