a = [1, 2, 3]
b = [4, 5, 6]

sum_ab = list(map(lambda x, y: x + y, a, b))
print(sum_ab)

countries = ["한국", "일본", "프랑스", "독일"]
capitals = ["서울", "도쿄", "파리", "베를린"]

sum_c_c = list(map(lambda x, y: f"{x}의 수도는 {y}입니다.", countries, capitals))
print(sum_c_c)
