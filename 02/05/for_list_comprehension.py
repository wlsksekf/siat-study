numbers = []
for i in range(5):
    numbers.append(2*i)
print(numbers)

c_numbers = [i*2 for i in range(5)]
print(c_numbers)

evens = []
for i in range(10):
    if i % 2 == 0:
        evens.append(i)
print(evens)

c_evens = [i for i in range(10) if i % 2 == 0]
print(c_evens)

result = []
for i in range(5):
    if i % 2 == 0:
        result.append('짝수')
    else:
        result.append('홀수')
print(result)

c_result = ['짝수' if i % 2 == 0 else '홀수' for i in range(5)]
print(c_result)