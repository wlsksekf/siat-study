import numpy as np

z = np.zeros((2, 3))
print(z)

o = np.ones(5)
print(o)

f = np.full((2, 3), 5)
print(f)

f_float = np.full((2, 3), 5, dtype=float)
print(f_float)

print(np.arange(1, 10))

print(np.arange(1, 10, 2))

print(np.arange(0, 1, 0.2))

original = [1, 2, 3]

add_10 = [x + 10 for x in original]

print(add_10)

np_result = np.array(original) + 10
print(np_result)

# 브로드캐스팅: 배열 전체를 한 번에 연산할 수 있음
# https://numpy.org/doc/stable/user/basics.broadcasting.html
a = np.array([1.0, 2.0, 3.0])
b = 2.0
print(a*b)