numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:5] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:5] = [20, 30, 40, 50]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:6] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:5:1] = [20, 30, 40, 50]
print(numbers)

# numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# numbers[2:5:2] = [20, 30, 40, 50]
# print(numbers) # error

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:2] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:-2] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 20, 30, 40, 9, 10]
numbers[2:-2] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[-5:-2] = [20, 30, 40]
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:5] = []
print(numbers)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers[2:-2] = []
print(numbers)