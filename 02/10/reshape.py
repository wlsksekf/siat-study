import numpy as np

arr = np.arange(6)
print(arr)

print(arr.reshape(2, 3))
print(arr.reshape(3, 2))

arr = np.arange(12)
new_arr = arr.reshape(-1, 4)

print(new_arr.shape)
print(new_arr)