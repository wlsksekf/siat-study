def process_account(account, amount):
    if amount <= 0:
        raise ValueError("결제 금액 오류")
    account.withdraw(amount)

def get_info(account):
    if hasattr(account, 'get_card_info'):
        return account.get_card_info()
    elif hasattr(account, 'get_info'):
        return account.get_info()
    return f"잔액: {account.get_balance()}원"