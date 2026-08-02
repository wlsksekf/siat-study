class MyList:
    def __init__(self, items):
        self.items = items
    
    def __setitem__(self, index, value):
        self.items[index] = value
    
lst = MyList([1, 2, 3])
lst[1] = 99

print(lst.items)

class Vector:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    
    def __repr__(self):
        return f"Vector({self.num1}, {self.num2})"
    
    def __add__(self, other):
        return Vector(self.num1 + other.num1, self.num2 + other.num2)

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)