import math

class Rectangle:
    def get_rect_area(self, width, height):
        return width * height

class Circle:
    def get_circle_area(self, radius):
        return math.pi * (radius ** 2)

class ShapeCalculator(Rectangle, Circle):
    pass

calc = ShapeCalculator()

rect = calc.get_rect_area(3, 4)
circle = calc.get_circle_area(2)

print(f"사각형의 넓이: {rect}")
print(f"원의 넓이: {circle}")