from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        """결제 수행"""
        pass

    @abstractmethod
    def cancel(self, amount):
        """결제 취소"""
        pass

