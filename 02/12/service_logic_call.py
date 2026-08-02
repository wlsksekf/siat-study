from service_logic import process_payment as pp
from BankTransferPayment import BankTransferPayment as bp
from CardPayment import CardPayment as cp
from KakaoPay import KakaoPaymemt as kp

pp(cp(), 10000, cancel=True)
pp(bp(), 20000, cancel=False)
pp(kp(), 30000, cancel=True)