# 1. 요구사항
#    (1) 함수 이름: create_wallet(owner, initial_balance=0)
#    (2) 매개변수 : owner: 지갑 주인의 이름 (문자열)
#                   initial_balance: 초기 잔액 (기본값 0)
#    (3) 기능
#        -  함수 내부에 balance 변수를 선언하여 잔액을 관리합니다.
#        -  spend(amount): 잔액보다 큰 금액을 쓰려고 하면 "OOO님, 잔액이 부족합니다! (잔액: 500원)" 메시지를 반환합니다.
#                          잔액이 충분하면 금액을 차감하고 "20,000원 지출. (남은 잔액: 30,000원)" 처럼 메시지를 반환합니다.
#        -  deposit(amount): 전달받은 금액만큼 잔액을 추가하고 "10,000원 입금. (현재 잔액: 40,000원)" 처럼 메시지를 반환합니다.
#        -  반환값 (Return): 위의 spend와 deposit 함수 자체를 딕셔너리(dict) 형태에 담아 반환합니다.
#                         키(key) 이름은 각각 "spend"와 "deposit"으로 설정합니다.
#    (4) 힌트
#        -  내부 함수에서 외부 함수의 변수인 balance를 수정하려면 nonlocal 키워드를 사용해야 합니다.
#        -  클로저를 활용하면 my_wallet = create_wallet("Alice")와 같이 실행했을 때, Alice만의 독립적인 메모리 공간(상태)이 유지됩니다.
# (5) 사용예시
#        # 사용 예시 - 지갑 잔액이 50000원 인데 20000원을 사용하는 경우와 10000원을 입금하는 경우
#         my_wallet = create_wallet("Alice", 50000)
#         print(my_wallet["spend"](20000))  # 20,000원 지출. (남은 잔액: 30,000원)
#         print(my_wallet["deposit"](10000)) # 10,000원 입금. (현재 잔액: 40,000원)

#        # 사용예시 - 지갑 잔액이 500원 인데 2000원을 사용하는 경우와 100000원을 입금하는 경우
#         my_wallet = create_wallet("Dooli", 500)
#         print(my_wallet["spend"](20000))    # Dooli님, 잔액이 부족합니다! (잔액: 500원)
#         print(my_wallet["deposit"](100000)) # 100,000원 입금. (현재 잔액: 100,500원)

# def create_wallet(owner, initial_balance=0):
#     spend(amount):
#         print()
#     deposit(amount):
#         print()

#     return spend, deposit

def create_wallet(owner, initial_balance=0):
    balance = initial_balance

    def spend(amount):
        nonlocal balance
        if amount > balance:
            return f"{owner}님, 잔액이 부족합니다! (잔액: {balance}원)"

        balance -= amount
        return f"{amount:,}원 지출. (남은 잔액: {balance:,}원)"

    def deposit(amount):
        nonlocal balance
        balance += amount
        return f"{amount:,}원 입금. (현재 잔액: {balance:,}원)"

    return {
        "spend": spend,
        "deposit": deposit
    }

my_wallet = create_wallet("Alice", 50000)
print(my_wallet["spend"](20000))
print(my_wallet["deposit"](10000))

dooli_wallet = create_wallet("Dooli", 500)
print(dooli_wallet["spend"](20000))
print(dooli_wallet["deposit"](100000))