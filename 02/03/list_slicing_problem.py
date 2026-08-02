numbers = [1, 2, 3, 4, 5, 6, 7]
numbers[2:5] = [0, 0, 0]
print(numbers)

numbers = [4, 5, 6]
numbers[:0] = [1, 2, 3]
print(numbers)

numbers = [1, 2, 3]
numbers[len(numbers):] = [4, 5, 6]
print(numbers)

numbers = [0, 0, 0, 0, 0]
numbers[::2] = [1, 1, 1]
print(numbers)

numbers = [1, 2, 3, 4, 5]
numbers = []
print(numbers)

numbers = [1, 2, 5, 6]
numbers[2:2] = [3, 4]
print(numbers)

