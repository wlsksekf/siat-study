from Account_logic import process_account as pa
from Account_logic import get_info as gi
from DebitCard import DebitCard as dc
from PointCard import PointCard as pc

# 문제 2
debit_card = dc("지민", 50000)
pa(debit_card, 20000)

print("\n--- 잔액 초과 결제 시도 ---")
pa(debit_card, 40000)

print("\n--- 입금 후 재결제 ---")
debit_card.deposit(10000)
pa(debit_card, 40000)

print(f"\n--- {debit_card.owner}님의 직불카드 정보 ---")
print(gi(debit_card))

print("="*30)

# 문제 3
point_card = pc("지민", 10000)
point_card.deposit(10000)
pa(point_card, 5000)
print(gi(point_card))