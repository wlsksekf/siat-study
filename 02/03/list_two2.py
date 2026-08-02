matrix = [[1, 2], [3, 4]]
matrix.append([5, 6])
print(matrix)

list_a = [[1, 2]]
list_b = [[3, 4]]
combined = list_a + list_b
print(combined)

matrix = [[1, 1], [3, 3]]
matrix.insert(1, [2, 2])
print(matrix)

students = [["철수", 90], ["영희", 100]]
idx = students.index(["영희", 100])
print(idx)

data = [[10, 20], [30, 40]]
data.remove([10, 20])
print(data)

matrix = [[1, 2], [3, 4]]
matrix.clear()
print(matrix)

scores = [[2, "B"], [1, "A"], [3, "C"]]
scores.sort()
print(scores)

scores = [[1, "B"], [1, "A"], [1, "C"]]
scores.sort()
print(scores)
