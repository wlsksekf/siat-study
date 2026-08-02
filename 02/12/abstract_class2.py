from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "멍멍"

class Cat(Animal):
    def sound(self):
        return "야옹"

d = Dog()
c = Cat()

print(d.sound())
print(c.sound())
