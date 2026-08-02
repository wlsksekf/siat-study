from Payment_01 import Payment

class KakaoPaymemt(Payment):
    def pay(self, amount):
        print(f"카카오페이로 {amount}원 결제")

    def cancel(self, amount):
        print(f"카카오페이 결제 {amount}원 취소")
