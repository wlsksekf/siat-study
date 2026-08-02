students = []

# 5명 데이터 입력 받기

# [1번째 학생 정보 입력]
# 이름: 강하늘
# 국어 영어 수학 점수(공백 구분): 100 90 95

# [2번째 학생 정보 입력]
# 이름: 김철수
# 국어 영어 수학 점수(공백 구분): 82 88 80

# [3번째 학생 정보 입력]
# 이름: 이영희
# 국어 영어 수학 점수(공백 구분): 74 72 70

# [4번째 학생 정보 입력]
# 이름: 박민수
# 국어 영어 수학 점수(공백 구분): 60 55 65

# [5번째 학생 정보 입력]
# 이름: 최유리
# 국어 영어 수학 점수(공백 구분): 50 40 30

# 입력 완료 후 화면 출력 결과
# ============================================================
# 이름            국어    영어    수학    총점    평균    학점
# ------------------------------------------------------------
# 강하늘          100      90      95     285      95.00    A
# 김철수           82      88      80     250      83.33    B
# 이영희           74      72      70     216      72.00    C
# 박민수           60      55      65     180      60.00    D
# 최유리           50      40      30     120      40.00    F
# ------------------------------------------------------------
# 과목 총점       366     345     340
# 과목 평균        73      69      68
# ============================================================
# -----------------------------------------------------------
# - 학생별 총점, 평균, 학점 구하기
# - 과목별 총점 및 평균 계산
# - 학생 관련 정보는 딕셔너리에 저장합니다.
#   예)  {
#         "name": name, "kor": kor, "eng": eng, 
#         "math": math, "total": total, "avg": avg, "grade": grade
#     }

for i in range(5):
    print(f"[{i+1}번째 학생 정보 입력]")
    name = input("이름: ")
    scores = input("국어 영어 수학 점수(공백 구분): ").split()
    kor = int(scores[0])
    eng = int(scores[1])
    math = int(scores[2])
    
    total = kor + eng + math
    avg = round(total / 3, 2)
    
    if avg >= 90:
        grade = 'A'
    elif avg >= 80:
        grade = 'B'
    elif avg >= 70:
        grade = 'C'
    elif avg >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    student = {
        "name": name, "kor": kor, "eng": eng, 
        "math": math, "total": total, "avg": avg, "grade": grade
    }
    students.append(student)
    print()

total_kor, total_eng, total_math = 0, 0, 0

count = len(students)

print("\n" + "=" * 50)
print("이름\t국어\t영어\t수학\t총점\t평균\t학점")
print("-" * 50)

for s in students:
    print(f"{s['name']}\t{s['kor']}\t{s['eng']}\t{s['math']}\t{s['total']}\t{s['avg']:.2f}\t{s['grade']}")
    
    total_kor += s['kor']
    total_eng += s['eng']
    total_math += s['math']

print("-" * 50)
print(f"과목 총점\t{total_kor}\t{total_eng}\t{total_math}")
print(f"과목 평균\t{total_kor//count}\t{total_eng//count}\t{total_math//count}")
print("=" * 50)
