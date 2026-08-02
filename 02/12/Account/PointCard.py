from Account_01 import Account

class PointCard(Account):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)
        self.point = 0

    def deposit(self, amount):
        super().deposit(amount)
        if amount > 0:
            earned_point = int(amount * 0.001)
            self.point += earned_point
            print(f"[포인트 적립] {earned_point}P가 쌓였습니다. (총 포인트: {self.point}P)")

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            print(f"[출금] {amount}원 처리 완료. (잔액: {self._balance}원)")
        else:
            print("[출금 실패] 잔액이 부족합니다.")

    def get_info(self):
        return f"{self.owner}님의 카드 상태 - 잔액: {self._balance}원, 포인트: {self.point}P"