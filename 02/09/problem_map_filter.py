# * 쇼핑몰 고객 데이터 전처리

# 여러 고객의 주문 내역이 담긴 리스트가 있습니다. 
# 각 고객의 주문 합계가 100,000원 이상인 고객을 대상으로, 
# 10% 할인을 적용한 최종 결제 금액 리스트를 생성하세요.

# - 데이터: orders = [120000, 45000, 200000, 95000, 150000]

# - 조건 1: filter를 사용하여 100,000원 이상인 금액만 추출합니다.

# - 조건 2: map과 lambda를 사용하여 남은 금액에 0.9를 곱합니다.

# - 결과: [108000.0, 180000.0, 135000.0]

orders = [120000, 45000, 200000, 95000, 150000]

filtered_orders = filter(lambda x: x >= 100000, orders)

final_orders = map(lambda x: x * 0.9, filtered_orders)

result = list(final_orders)
print(result)

orders = [120000, 45000, 200000, 95000, 150000]

sale_list = [x * 0.9 if x >= 100000 else x for x in orders ]

# for i in range(len(orders)):
#     print(f"{orders[i]} => {sale_list[i]}")

for original, result in zip(orders, sale_list):
    print(f"{original} => {result}")
