a = 10 
b = 20
print(a, b)

a, b = 10, 20
print(a, b)

x, y, z = 1, 2, 3
print(x, y, z)

first = 10
second = 20

imsi = first
first = second
second = imsi
print("2개의 숫자를 바꿈")
print(first)
print(second)

a, b = 10, 20
a, b = b, a
print(a, b)

a, *b = 1, 2, 3
print(a)
print(b)

a, *b, c, d = 1, 2, 3, 4, 5, 6
print(a)
print(b)
print(c)
print(d)

a, *b, c = 1, 2
print(a)
print(b)
print(c)