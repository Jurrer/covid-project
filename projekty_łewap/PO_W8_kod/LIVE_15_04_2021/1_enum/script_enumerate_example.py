car_type = ["CABRIOLET", "SUV", "COUPE"]
print(list(enumerate(car_type)))
i = 0

for idx, car_t in enumerate(car_type):
    print(idx, car_t)
    i += 1
