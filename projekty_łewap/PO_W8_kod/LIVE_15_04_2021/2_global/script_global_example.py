age = 18


def display_age():
    print("Age: %d" % age)


def set_new_age(new_age):
    age = new_age
    print(f"Inside set_new_age. Age: {age}")


display_age()
set_new_age(20)
display_age()
