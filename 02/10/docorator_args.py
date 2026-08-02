def decorator_with_args(func):
    def wrapper(*args, **kwargs):
        print("--- 함수 실행 시작 ---")
        print(f"인자: args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)
        print(result)

        print("--- 함수 실행 종료 ---")

        return result
    return wrapper

@decorator_with_args
def greet(name, **kwargs):
    return f"{name}님, 안녕하세요! (전달된 정보: {kwargs})"

greet("홍길동")
greet("홍길동", city="서울", age=25, hobby="코딩")