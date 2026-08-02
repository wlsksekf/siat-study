numbers = [0, 1, 2, 3]

# new_numbers = numbers.append(7)
# print(new_numbers)

# print(numbers)

numbers.append(7)
print(numbers)

numbers.insert(2, 8)
print(numbers)

a = [4, 5, 6]
numbers.extend(a)
print(numbers)

a = [0, 1, 2, 3]
numbers.remove(2)
print(numbers)

new_numbers = numbers.pop(1)
print(new_numbers)
print(numbers)


