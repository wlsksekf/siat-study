names = ["Kim", "Lee"]
ages = [20, 25]

zipped = zip(names, ages)

result = list(zipped)

print(result[0])
print(type(result[0]))

empty = list(zipped)
print(f"값이 비었나요? => {empty}")