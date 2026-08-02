name = "Alice"
age = 25
height = 165.5
is_Student = True

age_float = float(age)
print(age_float)

pi = float("3.141592")
print(pi)

pi = float(is_Student)
print(pi)

age_str = str(age)
print(f"형 변환 결과: {age_str}는 {type(age)} => {type(age_str)}")

print(str(is_Student))

height_int = int(height)
print(f"형 변환 결과: {height_int}는 {type(height)} => {type(height_int)}")

p = int("3")
print(p)

is_Student_int = int(is_Student)
print(is_Student_int)

print(bool(0))
print(bool(""))
print(bool(None))
