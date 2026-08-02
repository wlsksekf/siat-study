class Calculator:
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def is_positive(number):
        return number > 0
    
print(Calculator.add(10, 20))
print(Calculator.is_positive(-5))