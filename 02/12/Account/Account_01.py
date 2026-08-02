from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount):
        """
        입금 로직(모든 카드 공통)
        """
        if amount > 0:
            self._balance += amount

    @abstractmethod
    def withdraw(self, amount):
        """
        출금 로직
        """
        pass

    def get_balance(self):
        return self._balance
