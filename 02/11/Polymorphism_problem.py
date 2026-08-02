# 1. 도형을 표현하는 Shape 클래스를 정의하세요.
#     - area() 메서드를 정의하고, 기본 반환값은 0으로 합니다.

# 2. Shape 클래스를 상속받는 Rectangle 클래스를 정의하세요.
#     - 생성자에서 width, height를 받아 인스턴스 변수로 저장합니다.
#     - area() 메서드를 오버라이딩하여 사각형의 넓이(width × height)를 반환하도록 구현하세요.

# 3. Shape 클래스를 상속받는 Circle 클래스를 정의하세요.
#     - 생성자에서 radius를 받아 인스턴스 변수로 저장합니다.
#     - area() 메서드를 오버라이딩하여 원의 넓이(π × radius²)를 반환하도록 구현하세요.
#     - 원주율은 math.pi를 사용합니다. (import math)

# 4. 임의의 도형 객체를 받아 넓이를 계산하는 get_area() 함수를 작성하세요.
#     - 매개변수로 전달된 객체의 area() 메서드를 호출하여 그 결과를 반환하도록 합니다.
#     - 이 함수는 객체의 실제 타입과 관계없이 동일하게 동작해야 합니다.

# 5. Rectangle(3, 4)와 Circle(2) 객체를 생성하여 get_area() 함수에 전달하고,

#     각각의 넓이를 출력하세요.

import math

class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

def get_area(shape_obj):
    return shape_obj.area()

rect = Rectangle(3, 4)
cir = Circle(2)

get_area(rect)
get_area(cir)

print(f"사각형의 넓이: {get_area(rect)}")
print(f"원의 넓이: {get_area(cir)}")