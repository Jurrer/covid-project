from student import Student

stud_1 = Student("Kubuś", "Puchatek", 19)
stud_2 = Student("Prosiaczek", "OdKubusia", 23)
stud_3 = Student("Kubuś", "Puchatek", 20)

students = {stud_1, stud_2, stud_3}

for stud in students:
    print(stud)
print(stud_1 == stud_3)
print(stud_1.__hash__() == stud_3.__hash__())

print(stud_1.__eq__(stud_3))

print(stud_3 in students)
