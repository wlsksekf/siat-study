orders_data = [
    {"user": "Alice", "items": [15000, 20000, 5000]}, 
    {"user": "Bob", "items": [50000, 70000]},         
    {"user": "Charlie", "items": [3000, 2000]},       
    {"user": "Alice", "items": [10000]},              
]

# - 위 데이터를 이용해서 총 구매액을 구하고 아래와 같이 회원 등급 조건에 따라 딕셔너리로 완성해 주세요.
# - {'Alice': (50000, 'GOLD'), 'Bob': (120000, 'VIP'), 'Charlie': (5000, 'SILVER')}

# 고객명  총 구매액       회원 등급
# ----------------------------------------
# Alice     50,000원      GOLD
# Bob      120,000원      VIP
# Charlie    5,000원      SILVER

# 조건) 총 구매액이 100000 이상이면 "VIP"
#       30000 - 99999 이상이면 "GOLD"
#       아니면 "SILVER"

totals = {}
for order in orders_data:
    user, items = order["user"], order["items"]
    
    totals[user] = totals.get(user, 0) +sum(items)

di = {
    user: (total, "VIP" if total >= 100000 else "GOLD" if total >= 30000 else "SILVER")
    for user, total in totals.items()
}

print(di)

print(f"{'고객명':<10} {'총 구매액':<10} {'회원 등급'}")
print("-" * 50)
for user, (total, grade) in di.items():
    print(f"{user:<10} {total:>7,d}원       {grade}")