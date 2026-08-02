nums = [5, 2, 9, 1, 7]
sorted_nums = sorted(nums)
print(sorted_nums)
print(nums)

sorted_nums_desc = sorted(nums, reverse=True)
print(sorted_nums_desc)

words = ["apple", "banana", "kiwi", "cherry"]

sorted_words = sorted(words, key=len)
print(sorted_words)

students = [("Kim", 82), ("Lee", 91), ("Park", 78)]

sorted_student = sorted(students, key=lambda x: x[1])
print(sorted_student)

students = [("Kim", 82), ("Lee", 91), ("Park", 78)]

sorted_student = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_student)

students = [
    ("Kim", 82),
    ("Lee", 91), 
    ("Park", 82),
    ("Choi", 91),
    ("Han", 78)
]

sorted_student = sorted(students, key=lambda x: (x[1], x[0]))

print(sorted_student)