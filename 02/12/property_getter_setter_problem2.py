# 다음 조건에 맞는 클래스를 만들어 주세요
# 1. 클래스 이름은 Account 입니다.

# 2. __init__: 객체 생성 시 예금주와 초기 잔액을 설정합니다.
#     소유주는 public 변수에 저장
#     balance는 외부에서 수정 불가한 변수에 저장

#     def __init__(self, owner, balance=0)
#         owner : 소유자 이름 
#         balance=0 : 잔액    
#         self.__transactions = []  # 거래 내역 리스트

# 3. 입금 메서드 작성
#     def deposit(self, amount): # amount는 입금액
#     입금액이 0보다 크면 잔액에 더하고 거래 내역 리스트에 "입금: +5000원" 형식으로 추가되도록 합니다.
#     화면에는 "5000원이 입금되었습니다."라고 출력되도록 합니다.
#     입금액이 0보다 작으면 "입금액은 0보다 커야 합니다." 라고 출력합니다.

# 4. 출금 메서드 작성
#    def withdraw(self, amount): # amount는 출금액
#    0 < 출금액 <= 잔액 이면 잔액에서 출금액을 빼고 거래 내역 리스트에 "출금: -2000원" 형식으로 추가되도록 합니다.
#    화면에는 "2000원이 출금되었습니다."라고 출력되도록 합니다.
#    만약 0 < 출금액 <= 잔액 조건이 아니면 "잔액이 부족하거나 잘못된 금액입니다." 라고 출력합니다.


# 5. @property 사용
#    잔액을 확인할 때는 my_acc.balance처럼 변수처럼 편하게 사용하도록 메서드를 만듭니다.

# 6. __str__: 아래와 같이 출력되도록 합니다.
#    my_acc = Account("김철수", 1000)
#    print(my_acc)  # 김철수님의 계좌 (현재 잔액: 14000원)

# 7. __len__: len(my_acc)를 통해 이 계좌에서 발생한 총 거래 건수를 바로 알 수 있습니다.
#    총 거래 횟수: 3회
# Messages addressed to "meeting group chat" will also appear in the meeting group chat in Team Chat

# 서울맞춤훈련센터 11:00 AM
# 8. __iter__ (yield): 복잡한 인덱스 관리 없이 for문을 통해 거래 내역을 순차적으로 꺼내올 수 있게 합니다.
#    #  입금 및 출금
#    my_acc.deposit(5000)
#    my_acc.withdraw(2000)
#    my_acc.deposit(10000)

#    --- 거래 내역 목록 ---
#     입금: +5000원
#     출금: -2000원
#     입금: +10000원

# ======= [최종 출력] ============
# 5000원이 입금되었습니다.
# 2000원이 출금되었습니다.
# 10000원이 입금되었습니다.

# 김철수님의 계좌 (현재 잔액: 14000원)

# 현재 잔액(Property): 14000원

# 총 거래 횟수: 3회

# --- 거래 내역 목록 ---
# 입금: +5000원
# 출금: -2000원
# 입금: +10000원

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        self.__transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(f"입금: +{amount}원")
            print(f"{amount}원이 입금되었습니다.")
        else:
            print("입금액은 0보다 커야 합니다.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(f"출금: -{amount}원")
            print(f"{amount}원이 출금되었습니다.")
        else:
            print("잔액이 부족하거나 잘못된 금액입니다.")

    @property
    def balance(self):
        return self.__balance

    def __str__(self):
        return f"{self.owner}님의 계좌 (현재 잔액: {self.__balance}원)"

    def __len__(self):
        return len(self.__transactions)

    def __iter__(self):
        for transaction in self.__transactions:
            yield transaction

my_acc = Account("김철수", 1000)

my_acc.deposit(5000)
my_acc.withdraw(2000)
my_acc.deposit(10000)

print()
print(my_acc)
print()
print(f"현재 잔액(Property): {my_acc.balance}원")
print()
print(f"총 거래 횟수: {len(my_acc)}회")
print()
print("--- 거래 내역 목록 ---")
for log in my_acc:
    print(log)