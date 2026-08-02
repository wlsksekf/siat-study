class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"안녕하세요, 저는 {self.name}입니다.")

class Student(Person):
    def greet(self):
        print(f"안녕하세요, 저는 학생 {self.name}입니다.")

    def study(self):
        print(f"{self.name}이(가) 공부합니다.")

class Teacher(Person):
    def greet(self):
        print(f"안녕하세요, 저는 선생님 {self.name}입니다.")

    def teach(self):
        print(f"{self.name} 선생님이 수업을 합니다.")

person = Person("영희")
student = Student("철수")
teacher = Teacher("민수")

student.greet()
student.study()

teacher.greet()
teacher.teach()