from Payment_01 import Payment

class BankTransferPayment(Payment):

    def pay(self, amount):
        print(f"계좌이체로 {amount}원 결제")

    def cancel(self, amount):
        print(f"계좌이체 {amount}원 취소")
