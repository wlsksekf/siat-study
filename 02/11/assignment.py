# m1 = Matrix([[1, 2], [3, 4]])
# m2 = Matrix([[5, 6], [7, 8]])

# # 동작 원리: m1 + m2 -> m1.__add__(m2) 호출
# result = m1 + m2

# print("Matrix 1:", m1)
# print("Matrix 2:", m2)
# print("결과 (m1 + m2):", result)

# ========================
# Matrix 1: Matrix(
#   [1, 2]
#   [3, 4]
# )
# Matrix 2: Matrix(
#   [5, 6]
#   [7, 8]
# )
# 결과 (m1 + m2): Matrix(
#   [6, 8]
#   [10, 12]
# )

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __add__(self, other):
        new_data = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            new_data.append(row)
        return Matrix(new_data)

    def __str__(self):
        result = "Matrix(\n"
        for row in self.data:
            result += f"  {row}\n"
        result += ")"
        return result

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[5, 6], [7, 8]])

result = m1 + m2

print("Matrix 1:", m1)
print("Matrix 2:", m2)
print("결과 (m1 + m2):", result)