from armored_car import ArmoredCar
from car import Car

car_1 = Car("Mazda", "mx5", 2021)

armored_car_1 = ArmoredCar("Audi", "A8", 2019, 30)

print(car_1)
print(armored_car_1)
print(armored_car_1.create_secret_name())
