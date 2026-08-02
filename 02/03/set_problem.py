# 중복을 제거한 후
# 정렬된 리스트로 만들어 주세요

numbers = [1, 2, 2, 5, 3, 4, 4, 0]

result = sorted(list(set(numbers)))

print(result)

print(sorted([5, 2, 4]))

print(sorted((5, 2, 4)))

print(sorted({5, 2, 4}))

print(sorted("python"))

print(sorted({"b": 2, "a": 1, "c": 3}))

d = {"b": 2, "a": 1, "c": 3}
print(sorted(d.items))

print(sorted(d.values))