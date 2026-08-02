class Student:
    school_name = "파이썬고등학교"

    def __init__(self, name, age):
        self.name = name
        self.age = age


    def introduce(self):
        print(f"안녕하세요, 저는 {Student.school_name}에 다니는 {self.name}이고 {self.age}살입니다.")

s1= Student("홍길동", 18)
s2= Student("김철수", 17)

s1.introduce()
s2.introduce()

print(Student.school_name)

print(s1.name, s1.age)
print(s2.name, s2.age)

print(s1.school_name)
print(s2.school_name)

Student.school_name = "AI고등학교"

print(s1.school_name)
print(s2.school_name)