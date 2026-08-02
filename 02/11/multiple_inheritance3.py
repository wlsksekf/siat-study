import math

class Rectangle:
    def area(self, width, height):
        return width * height

class Circle:
    def area(self, width, height):
        return (width+height)/2

class ShapeCalculator(Rectangle, Circle):
    pass

calc = ShapeCalculator()

rect = calc.area(3, 4)
tri = calc.area(2, 3)

print(f"사각형의 넓이: {rect}")
print(f"삼각형의 넓이: {tri}")

print(ShapeCalculator.mro())