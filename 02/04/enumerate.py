fruits = ["apple", "banana", "cherry"]
for index, name in enumerate(fruits):
    print(f"{index}번 과일: {name}")

names = ["Kim", "Lee"]
ages = [20, 25]

zipper = zip(names, ages)
list1 = list(zipper)

for i, (name, age) in enumerate(list1):
    print(f"{i}번 이름: {name} 나이: {age}")