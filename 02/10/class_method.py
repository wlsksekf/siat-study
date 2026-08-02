class Student:
    count = 0

    def __init__(self):
        Student.count += 1

    @classmethod
    def print_count(cls):
        print(f"{cls.count}명이 입학했습니다.")

Student.print_count()

kim = Student()
Student.print_count()

lee = Student()
Student.print_count()

kim.print_count()