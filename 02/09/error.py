if True:
    print("Hello")

try:
    a = 10
    b = 0
    print(a / b)    
except ZeroDivisionError:
    print("division by zero")

try:
    num = int(input("정수를 입력하세요: "))
except ValueError:
    print("잘못된 숫자 입력")
else:
    print("입력한 숫자:", num)
finally:
    print("무조건 실행")

try:
    with open("info.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("파일이 없습니다.")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
except Exception:
    print("오류 발생")


