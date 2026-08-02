a = [i * 2 for i in range(5)]

b = (i * 2 for i in range(5))

print(type(a))
print(type(b))
print()

my_tuple = tuple(i * 2 for i in range(5))

print(my_tuple)
print(type(my_tuple))
print()

gen = (i * 2 for i in range(5))

for value in gen:
    print(value, end=" ")
print()

for value in gen:
    print("제가 보이나요?")
    print(value, end=",")

print("="*10)
gen = (i * 2 for i in range(5))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print("="*10)



