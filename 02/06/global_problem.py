print("="*5, "[출력결과]", "="*5)

count = 0

def increase():
    global count
    count += 1

for i in range(5):
    increase()
    print("함수 호출 후 count =", count)

print("최종 count =", count)