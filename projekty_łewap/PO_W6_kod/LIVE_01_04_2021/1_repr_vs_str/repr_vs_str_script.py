from group import Group
from human import Human

human_1 = Human("Kaczka", "Dziwaczka")
human_2 = Human("Śpiąca", "Królewna")
human_3 = Human("Miś", "Uszatek")

group = Group()
group.add(human_1)
group.add(human_2)
group.add(human_3)

print(human_1)

print(group)
