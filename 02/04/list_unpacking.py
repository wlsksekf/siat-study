numbers = [1, 2, 3]
a, b, c = numbers
print(a, b, c)
print()

numbers = [1, 2, 3, 4, 5]
a, *b, c = numbers
print(a)
print(b)
print(c)
print()

first, *others = [10, 20, 30, 40]
print(first)
print(others)
print()

*others, last = [10, 20, 30, 40]
print(others)
print(last)
print()

def add(x, y, z):
    return x + y + z

nums = [10, 20, 30]
print(add(*nums))

students = [["Kim", 90], ["Lee", 85]]

for name, score in students:
    print(name, score)