person = {"name": "Alice", "age": 25}

person["age"] = 26
person["city"] = "Seoul"
print("age 수정 및 city 추가: ", person)

removed = person.pop("city")

print("최종 딕셔너리: ", person)
print("삭제된 값: ", removed)

print(person.keys())

print(person.values())

print(person.items())

person.clear()
print(person)

