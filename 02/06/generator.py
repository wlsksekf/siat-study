def count_up(n):
    result = []
    for i in range(n):
        result.append(i)
    return result

c = count_up(5)
print(c)

def g_count_up(n):
    for i in range(n):
        yield i

gen = g_count_up(3)
print(gen)

print(next(gen))
print(next(gen))
print(next(gen))

for x in gen:
    print("내가 출력됨?")
    print(x)

gen = g_count_up(3)
for x in gen:
    print(f"다시 만들어서 출력해:{x}")