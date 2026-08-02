# 1. 5행 4열 데이터 생성
students = [
    ["이철수", 90, 80, 100],
    ["김영희", 100, 80, 90],
    ["최길동", 85, 70, 75],
    ["박민수", 95, 85, 80],
    ["정수지", 80, 95, 90]
]

# print("이름 국어 영어 수학 총점")
# print("--------------------------")
# print(f"{students[0][0]} {students[0][1]} {students[0][2]} {students[0][3]} {sum(students[0][1:4])}")
# print(f"{students[1][0]} {students[1][1]} {students[1][2]} {students[1][3]} {sum(students[1][1:4])}")
# print(f"{students[2][0]} {students[2][1]} {students[2][2]} {students[2][3]} {sum(students[2][1:4])}")
# print(f"{students[3][0]} {students[3][1]} {students[3][2]} {students[3][3]} {sum(students[3][1:4])}")
# print(f"{students[4][0]} {students[3][1]} {students[3][2]} {students[3][3]} {sum(students[3][1:4])}")
# print("--------------------------")
# print(f"총점 {students[0][1]+students[1][1]+students[2][1]+students[3][1]+students[4][1]} {students[0][2]+students[1][2]+students[2][2]+students[3][2]+students[4][2]} {students[0][3]+students[1][3]+students[2][3]+students[3][3]+students[4][3]}")

s1, s2, s3, s4, s5 = students

kor_scores = [s1[1], s2[1], s3[1], s4[1], s5[1]]
eng_scores = [s1[2], s2[2], s3[2], s4[2], s5[2]]
math_scores = [s1[3], s2[3], s3[3], s4[3], s5[3]]

kor_total = sum(kor_scores)
eng_total = sum(eng_scores)
math_total = sum(math_scores)

print("이름 국어 영어 수학 총점")
print("--------------------------")
print(s1)
print(s2)
print(s3)
print(s4)
print(s5)
print("--------------------------")
print(f"총점\t{kor_total}\t{eng_total}\t{math_total}")