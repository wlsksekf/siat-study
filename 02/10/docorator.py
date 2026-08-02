def my_decorator(func):
    def wrapper():
        print("--- 함수 실행 시작 ---")
        func()
        print("--- 함수 실행 종료 ---")

    return wrapper

@my_decorator
def hello():
    print("안녕하세요!")

hello()