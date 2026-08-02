# x = 10

# def func():
#     x = x + 5
#     print("함수 내부 x:", x)

# func()
# print("함수 외부 x:", x)

x = 10

def func():
    global x
    x = x + 5
    print("함수 내부 x:", x)

func()
print("함수 외부 x:", x)