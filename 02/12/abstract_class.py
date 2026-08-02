from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def sound(self):
        """이 메서드는 자식 클래스에서 반드시 구현해야 함"""
        pass

try:
    a = Animal()
except TypeError as e:
    print(f"에러 발생: {e}") # Can't instantiate abstract class Animal without an implementation for abstract method 'sound'

class Bird(Animal):
    pass

# b = Bird() - 에러 Can't instantiate abstract class Animal without an implementation for abstract method 'sound'