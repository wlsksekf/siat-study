class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"__str__이름: {self.name}"

    def __repr__(self):
        return f"Person('{self.name}')"

p1 = Person("Alice")
print(p1)

people = [Person("Alice"), Person("Bob")]
print(people)

print(repr(people))
