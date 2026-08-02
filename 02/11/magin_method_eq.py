class Student:
    def __init__(self, student_id):
        self.student_id = student_id

    def __eq__(self, other):
        return self.student_id == other.student_id

s1 = Student(101)
s2 = Student(101)

print(id(s1))
print(id(s2))
print(s1 == s2)