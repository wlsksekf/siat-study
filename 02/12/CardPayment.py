from Payment_01 import Payment

class CardPayment(Payment):

    def pay(self, amount):
        print(f"카드로 {amount}원 결제")

    def cancel(self, amount):
        print(f"카드 결제 {amount}원 취소")
