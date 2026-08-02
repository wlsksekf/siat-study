from MyError import MyError

def check_number(n):
    if n < 0:
        raise MyError("음수는 허용 안 됨")
    return n * 2

try:
    result = check_number(-5)
    print("결과:", result)
except MyError as e:
    print("사용자 정의 에러 발생!")
    print("사용자 정의 에러 메시지:", e)