student = ("Kim", 90)

name, score = student
print(name)
print(score)

students = [("Kim", 90), ("Lee", 85), ("Park", 95)]

for name, score in students:
    print(name, score)

numbers = (1, 2, 3, 4, 5)

a, *b, c = numbers
print(a)
print(b)
print(c)

def add(x, y, z):
    return x + y + z

nums = (10, 20, 30)

print(add(*nums))

data = ("Alice", (90, 95, 100))
name, (math, eng, sci) = data
print(name)
print(math)
print(eng)
print(sci)