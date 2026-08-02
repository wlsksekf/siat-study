# 1. 자동차 클래스 만들기
#    (1) 클래스 이름은 Car로 정합니다.
#    (2) 클래스 변수: 모든 자동차가 공유하는 wheels 변수를 만들고 값으로 4를 할당하세요.
#    (3) 생성자 메서드 (__init__): 자동차를 만들 때 brand(브랜드)와 color(색상)를 입력받아 저장하도록 만드세요.
#    (4) info() 메서드: 호출 시 해당 자동차의 브랜드, 색상, 바퀴 개수를 문장으로 출력합니다.
#    (5) drive() 메서드: 호출 시 해당 자동차의 브랜드를 언급하며 "주행을 시작합니다"라는 메시지를 출력합니다.

# 2. 두 대의 자동차 객체를 만드세요.
#    c1: 브랜드 "현대", 색상 "red"
#    c2: 브랜드 "기아", 색상 "blue"

# 3. 생성된 두 자동차의 info()와 drive() 메서드를 각각 호출하여 결과를 확인하세요.

# 4. 출력 예시

#     이 차는 현대 브랜드의 red색 자동차입니다.
#     바퀴는 4개가 달려 있습니다.
#     현대 자동차가 주행을 시작합니다! 
#     ------------------------------
#     이 차는 기아 브랜드의 blue색 자동차입니다.
#     바퀴는 4개가 달려 있습니다.
#     기아 자동차가 주행을 시작합니다!

class Car:
    wheels = 4

    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def info(self):
        print(f"이 차는 {self.brand} 브랜드의 {self.color}색 자동차입니다.")
        print(f"바퀴는 {Car.wheels}개가 달려 있습니다.")

    def drive(self):
        print(f"{self.brand} 자동차가 주행을 시작합니다!")

c1 = Car("현대", "red")
c2 = Car("기아", "blue")

c1.info()
c1.drive()
print("-"*30)
c2.info()
c2.drive()