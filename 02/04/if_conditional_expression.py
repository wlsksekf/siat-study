num = 3

if num % 2 == 0:
    result = '짝수'
else:
    result = '홀수'
print(result)

result = '짝수' if num % 2 == 0 else '홀수'
print(result)

result = ['짝수' if num % 2 == 0 else '홀수' for i in range(5)]
print(result)