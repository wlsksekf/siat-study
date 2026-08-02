students = {'name': 'Alice', 'age': 26}

key1, key2 = students
print(key1, key2)
print()

value1, value2 = students.values()
print(value1, value2)
print()

for key, value in students.items():
    print(key, value)

print()

students = {'name': 'Alice', 'age': 26}
print(*students)
print()

info = {"name": "Kim"}
scores = {"kor": 90, "eng": 85}
full_data = {**info, **scores}
print(full_data)
print()

full_data = info | scores
print(full_data)
print()

def show_info(name, age):
    print(f"{name} is {age} years old.")

show_info(*students)
print()

show_info(**students)
print()