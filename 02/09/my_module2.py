def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

print("mym2의 name값은", __name__, "입니다.")

if __name__ == "__main__":
    print("이 코드는 mym2.py를 직접 실행했을 때만 보임")
    print(add(10, 20))