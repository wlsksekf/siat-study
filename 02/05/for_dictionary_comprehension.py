students = {'Alice': 90, 'Bob': 85}

new_students = {}

for name, score in students.items():
    new_students[name] = score + 5
print(new_students)

students2 = {'Alice': 90, 'Bob': 85}
c_new_students2 = {name: score + 5 for name, score in students2.items()}
print(c_new_students2)

students = {'Alice': 90, 'Bob': 85}
c_passed = {name: score for name, score in students.items() if score >= 90}
print(c_passed)

numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
c_numbers = {alphabet: ('even' if number % 2 == 0 else 'odd') for alphabet, number in numbers.items()}
print(c_numbers)





