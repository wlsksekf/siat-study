students = []

for i in range(5):
    print(f"\n[{i+1}번째 학생 정보 입력]")
    name = input("이름: ")
    kor, eng, math = map(int, input("국어 영어 수학 점수(공백 구분): ").split())
    
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

count = len(students)

print("\n" + "=" * 50)
print("이름\t국어\t영어\t수학\t총점\t평균\t학점")
print("-" * 50)

for s in students:
    print(f"{s['name']}\t{s['kor']}\t{s['eng']}\t{s['math']}\t{s['total']}\t{s['avg']:.2f}\t{s['grade']}")
    
total_kor =sum([s['kor'] for s in students])
total_eng =sum([s['eng'] for s in students])
total_math =sum([s['math'] for s in students])

print("-" * 50)
print(f"과목 총점\t{total_kor}\t{total_eng}\t{total_math}")
print(f"과목 평균\t{total_kor//count}\t{total_eng//count}\t{total_math//count}")
print("=" * 50)