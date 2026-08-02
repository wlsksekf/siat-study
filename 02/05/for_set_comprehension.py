names = ['apple', 'banana', 'cherry', 'apple', 'cherry', 'DRAGONFRUIT']
unique_fruits = {f.lower() for f in names}
print(unique_fruits)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 4, 6]
unique_numbers = {n for n in numbers if n > 5 and n % 2 == 0}
print(unique_numbers)

word = "abracadabra"
not_a = {w for w in word if w != 'a'}
print(not_a)

numbers = {1, 2, 3, 4, 5, 6}
unique_numbers2 = [num if num % 2 != 0 else num * 10 for num in numbers]
print(unique_numbers2)

