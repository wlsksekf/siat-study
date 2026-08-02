class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: [{self.name} {self.age}]"

obj = Person("Alice", 21)

print(obj)

print(str(obj))

print(obj.__str__())