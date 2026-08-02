x = 10

def func():
    y = 5
    print("함수 내부 x:", x)
    print("함수 내부 y:", y)

func()

print("함수 외부에서 전역 변수 x 접근:", x)
# print("함수 외부에서 전역 변수 y 접근:", y) 오류