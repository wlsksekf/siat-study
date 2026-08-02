def student_info(name="홍길동", age=20, grade="A"):
    return f"이름: {name}, 나이: {age}, 성적: {grade}"

response = student_info()
print(response)

# def introduce(name, age, city):
#     return f"이름: {name}, 나이: {age}, 도시: {city}"

# response = introduce(*input("이름, 나이, 도시를 입력하세요: ").split())
# print(response)

# 키워드 인자는 순서 자유

def introduce1(name, age, city):
    return f"이름: {name}, 나이: {age}, 도시: {city}"

response = introduce1("홍길동", city="대전", age="22")
print(response)
