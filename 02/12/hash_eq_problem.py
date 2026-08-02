class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.width == other.width and self.height == other.height
        return False

    def __hash__(self):
        return hash((self.width, self.height))

r1 = Rectangle(10, 20)
r2 = Rectangle(10, 20)
r3 = Rectangle(20, 10)

print(r1 == r2)
print(r1 == r3)

s = {r1, r2, r3}
print(len(s))