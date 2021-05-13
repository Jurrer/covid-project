from num_generator_type import NumGeneratorType

print(NumGeneratorType.RANDOM.name)
print(NumGeneratorType.RANDOM.value)
print(NumGeneratorType.ASCENDING.value)
print(NumGeneratorType.DESCENDING.value)


def data_generator(type):
    if type == NumGeneratorType.RANDOM:
        pass
    elif type == NumGeneratorType.ASCENDING:
        pass
