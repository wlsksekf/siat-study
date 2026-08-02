student = (1, 100, 80, 90, "A")

id, *scores, grade = student

print(f"id: {id}")
print(f"scores: {scores}")
print(f"총점: {sum(scores)}")
print(f"평균: {sum(scores)/len(scores)}")
print(f"등급: {grade}")