import random

def process_payment(payment, amount, cancel=False):
    if amount <= 0:
        raise ValueError("결제 금액 오류")
    
    if cancel:
        payment.cancel(amount)
    else:
        payment.pay(amount)