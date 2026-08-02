from Account_01 import Account

class DebitCard(Account):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)
        self._total_spent = 0
    
    def deposit(self, amount):
        if amount > 0:
            super().deposit(amount)

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            self._total_spent += amount
            print(f"[결제 성공] {self.owner}님 {amount}원 결제 완료.")
            print(f"현재 잔액: {self._balance}원")
        else:
            print("[결제 실패] 잔액이 부족합니다.")
            print(f"현재 잔액: {self._balance}원 / 부족 금액: {amount - self._balance}원")

    def get_card_info(self):
        return f"현재 잔액: {self._balance}원\n총 사용 금액: {self._total_spent}원"