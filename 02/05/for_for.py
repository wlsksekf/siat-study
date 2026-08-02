matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for col in row:
        print(col, end=" ")
    print()

for i in range(2, 10):
    for in_i in range(1, 10):
        print(f"{i} * {in_i} = {i*in_i}", end="\t")
    print()