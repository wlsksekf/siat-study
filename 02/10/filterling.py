import numpy as np

arr = np.array([1, 2, 3, 4])
print(arr > 2)

arr = np.array([10, 20, 30, 40])
result = arr[arr >= 30]
print(result)

arr = np.array([1, 2, 3, 4, 5])
print(arr[1:4])

arr = np.array([10, 20, 30])
print(arr[1])

arr = np.array([1, 2], [3, 4])
print(arr[0, 1])
