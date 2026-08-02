def add_all(*args):
    print(type(args))
    print(args)
    return sum(args)

print(add_all(10, 20))
print(add_all(1, 2, 3, 4, 5))