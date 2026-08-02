def add_no_return(a, b):
    result = a + b
print(add_no_return(3, 5))

def add_no_return(a, b):
    result = a + b
    return result
print(add_no_return(3, 5))

def welcome(name):
    response = (f"{name}님, 환영합니다!")
    return response

print(welcome(input("이름 입력: ")))


