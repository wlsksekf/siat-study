class Parent:
    def method_parent(self):
        print("부모 메서드 호출")

class Child(Parent):
    def __init__(self, name, age):
        self.age = age
        self.name = name

    def method_child(self):
        print("자식 메서드 호출")

c = Child("철수", 10)

c.method_child()
c.method_parent()

print(c.name)
print(c.age)