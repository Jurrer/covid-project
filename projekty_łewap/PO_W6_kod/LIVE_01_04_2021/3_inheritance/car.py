class Car:

    def __init__(self, mark, model, year_of_production):
        self.__mark = mark
        self.__model = model
        self.__year_of_production = year_of_production

    def __str__(self):
        cls_name = self.__class__.__name__
        attrs = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"[({cls_name}): {attrs}]"

    def __get_last_2_digits_of_year(self):
        return str(self.__year_of_production)[-2:]
