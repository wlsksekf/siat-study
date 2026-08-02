person = {"name": "Alice", "age": 25, "city": "Seoul"}
print(person)

person = {"name": "Alice", "age": 25}
print(person["name"])

print(person.get("city"))

print(person.get("city", "N/A"))


