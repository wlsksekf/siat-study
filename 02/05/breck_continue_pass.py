print(f"{'*'*10}break 문{'*'*10}")
for i in range(1, 10):
    if i == 5:
        print("반복 종료!")
        break
    print(i)

print(f"{'*'*10}continue 문{'*'*10}")
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

print(f"{'*'*10}pass 문{'*'*10}")
for i in range(1, 6):
    if i == 3:
        pass
    print(i)