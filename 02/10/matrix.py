import numpy as np

a = [
    [1, 2],
    [3, 4]
]

b = [
    [5, 6],
    [7, 8]
]

result = [
    [0, 0],
    [0, 0]
]

result[0][0] = a[0][0]*b[0][0] + a[0][1]*b[1][0]

result[0][1] = a[0][0]*b[0][1] + a[0][1]*b[1][1]

result[1][0] = a[1][0]*b[0][0] + a[1][1]*b[1][0]

result[1][1] = a[1][0]*b[0][1] + a[1][1]*b[1][1]
print(result)

n_a = np.array(a)
n_b = np.array(b)
print(n_a @ n_b)