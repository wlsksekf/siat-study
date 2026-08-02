class Product:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

p = Product(1000)
print(p.price)   # ← 메서드 price()를 변수처럼 사용z