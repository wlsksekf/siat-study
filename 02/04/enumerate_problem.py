names = ["홍길동", "이순신"]
scores = [100, 90]
grades = ["Best", "Good"]

zipper = zip(names, scores, grades)
list1 = list(zipper)

for i, (names, scores, grades) in enumerate(list1):
    print(f"{names}: {scores}점({grades})")