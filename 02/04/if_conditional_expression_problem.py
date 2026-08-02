num = -3
result = "양수" if num > 0 else "음수 또는 0"
print(result)

score = 58
status = "합격" if score >= 60 else "불합격"
print(status)

ch = ""
result = "비어 있음" if ch == "" else "값 있음"
print(result)

age = 17
result = "성인" if age >= 20 else "미성년자"
print(result)

num = 40
result = "10의 배수" if num % 10 == 0 else "아님"
print(result)

a = 7
b = 9
max_value = a if a > b else b
print(max_value)

a = 7
b = 9
min_value = a if a < b else b
print(min_value)

num = 0
result = "zero" if num == 0 else "non-zero"
print(result)

word = "python"
result = "긴 문자열" if len(word) >= 5 else "짧은 문자열"
print(result)

word = "level"
result = "회문입니다" if word == word[::-1] else "회문이 아닙니다"
print(result)