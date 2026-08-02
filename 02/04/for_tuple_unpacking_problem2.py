student = (1, 100, 80, 90)

id, *scores = student

average = sum(scores)/len(scores)

if average < 60:
    GPA = "F"
elif average >= 60 and average < 70:
    GPA = "D"
elif average >= 70 and average < 80:
    GPA = "C"
elif average >= 80 and average < 90:
    GPA = "B"
else:
    GPA = "A"

student = student + (GPA,)

print(f"id: {id}")
print(f"scores: {scores}")
print(f"평균: {average}")
print(f"학점: {GPA}")
print(f"최종 student: {student}")