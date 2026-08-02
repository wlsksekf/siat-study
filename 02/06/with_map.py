def square(x):
    return x ** 2

nums = [1, 2, 3, 4]
result = map(square, nums)
# print(list(result))
# for r in result:
#     print(r)
print(*result)

nums = [1, 2, 3, 4]
result = list(map(lambda x: x ** 2, nums))
print(result)

