# @logger
# def add(a, b):
#     return a + b

# @logger
# def greet(name, message="안녕하세요"):
#     return f"{name}님, {message}"
# =======================================================
# x = add(10, 20)

# [2026-02-10 15:46:44] [호출] 함수명: add/
# 인자: args=(10, 20), kwargs={}/
# [2026-02-10 15:46:44] [완료] 결과값: 30
# --------------------------------------------------
# y = greet("지민", message="반갑습니다")

# [2026-02-10 15:46:44] [호출] 함수명: greet
# 인자: args=('지민',), kwargs={'message': '반갑습니다'}
# [2026-02-10 15:46:44] [완료] 결과값: 지민님, 반갑습니다
# --------------------------------------------------

import datetime

def logger(func):
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{now}] [호출] 함수명: {func.__name__}")
        print(f"인자: args={args}, kwargs={kwargs}")
        
        result = func(*args, **kwargs)
        
        print(f"[{now}] [완료] 결과값: {result}")
        print("-" * 50)
        
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

@logger
def greet(name, message="안녕하세요"):
    return f"{name}님, {message}"

x = add(10, 20)
y = greet("지민", message="반갑습니다")