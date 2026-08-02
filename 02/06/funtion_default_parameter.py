def greet(name, msg="안녕하세요"):
    return f"{name}님, {msg}"

response = greet("김철수")
print(response)

response = greet("이영희", "좋은 하루!")
print(response)

# def greet_error(msg="안녕하세요", name):
#     return f"{name}님, {msg}"

