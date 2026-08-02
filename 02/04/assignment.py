students = [
    ["이철수", 90, 80, 100],
    ["김영희", 100, 80, 90],
    ["최길동", 85, 70, 75],
    ["박민수", 95, 85, 80],
    ["정수지", 80, 95, 90]
]

total_kor = 0
total_eng = 0
total_math = 0

print("="*50)
print("이름\t국어\t영어\t수학")
print("-"*50)

for s in students:
    print(s[0], "\t", s[1], "\t", s[2], "\t", s[3])
    total_kor += s[1]
    total_eng += s[2]
    total_math += s[3]

print("-"*50)
print("총점\t", total_kor, "\t", total_eng, "\t", total_math)